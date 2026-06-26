"""
Core HTTP session for the WarEra tRPC API.

Two call modes:
  • Single  → GET  /trpc/<procedure>?input=<url-encoded JSON>
  • Batch   → POST /trpc/<proc0>,<proc1>,...?batch=1   body: {"0": input0, ...}

Auth is optional: X-API-Key header is injected only when a key is present.

Rate-limit handling: the API returns standard rate-limit headers on every response:
  ratelimit-limit:     total requests allowed in the current window
  ratelimit-remaining: requests remaining in the current window
  ratelimit-reset:     seconds until the window resets

Rather than using a hardcoded delay, this session reads these headers after every
response and automatically waits when remaining reaches 0, for exactly as long as
the server says it will take for the window to reset.  This means the client
self-adapts to any future changes the server makes to its rate-limit policy.

Retry logic covers 429 (rate limit) and 5xx errors with exponential backoff.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import random
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import httpx
import orjson as _orjson  # ~5-10× faster JSON serialization
from tenacity import (
    AsyncRetrying,
    before_sleep_log,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
    wait_random_exponential,
)

from ._swr import SWRCache
from .exceptions import (
    WareraBatchError,
    WareraError,
    WareraHTTPError,
    WareraRateLimitError,
    WareraValidationError,
    _raise_for_status,
)

logger = logging.getLogger("warera.http")

# Public constant so client.py can import it instead of duplicating the string.
DEFAULT_BASE_URL = "https://api2.warera.io/trpc"


@dataclass(frozen=True)
class RetryInfo:
    """
    Details passed to the ``on_retry`` callback just before each retry sleep.

    Attributes:
        attempt:     The attempt number that just failed (1-based — the first
                     retry receives ``attempt=1``).
        delay_s:     Seconds the client will sleep before the next attempt.
        error:       The exception that triggered the retry.
        status_code: HTTP status of the failure, when it was an HTTP error
                     (``None`` for pure network/transport errors).
    """

    attempt: int
    delay_s: float
    error: BaseException | None
    status_code: int | None = None


OnRetryCallback = Callable[[RetryInfo], None]
_ENV_KEY = "WARERA_API_KEY"


def _get_rt_header() -> str:
    default_retryable_status_codes = [408, 409, 425, 429, 500, 502, 503, 504]

    def to_base36(num: int) -> str:
        if num == 0:
            return "0"
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        res = ""
        while num > 0:
            num, rem = divmod(num, 36)
            res = chars[rem] + res
        return res

    return ".".join(
        to_base36(status * (index + 3) + index)
        for index, status in enumerate(default_retryable_status_codes)
    )


_RT_HEADER = _get_rt_header()


# Moved into HttpSession as an instance method.


class _RateLimitState:
    """
    Tracks the server-reported rate-limit window and enforces waits when
    the remaining quota hits zero.

    The API returns three headers per response:
      ratelimit-limit     – max requests per window (e.g. 500)
      ratelimit-remaining – requests left in the current window (e.g. 490)
      ratelimit-reset     – seconds until the window resets (e.g. 43)

    After each response we record ``remaining`` and compute the absolute
    monotonic timestamp at which the window will reset.  Before the next
    outgoing request we check whether we still have quota; if not, we
    sleep until the reset timestamp.

    Cumulative statistics are tracked across all window refreshes so
    callers can inspect total usage for the session's lifetime.
    """

    def __init__(self) -> None:
        self.limit: int | None = None
        self.remaining: int | None = None
        # Absolute monotonic time (seconds) when the window resets.
        self._reset_at: float | None = None
        # Initialised eagerly by HttpSession._ensure_client() once an event
        # loop is running, so there is never a window where two coroutines
        # race to create the first Lock object.
        self._lock: asyncio.Lock | None = None

        # ── Cumulative stats (survive window refreshes) ──
        self.total_http_requests: int = 0  # raw HTTP requests (GET + POST)
        self.total_procedures: int = 0  # individual tRPC procedures called
        self.window_refreshes: int = 0  # times we waited for a window reset
        self.total_wait_seconds: float = 0.0  # total time spent sleeping on rate limits
        # Track per-window usage: when remaining jumps back up (window refresh
        # detected from headers), we finalize the previous window's consumption.
        self._prev_remaining: int | None = None
        self._prev_limit: int | None = None

    def ensure_lock(self) -> None:
        """Create the asyncio.Lock if it does not yet exist.

        Must be called from inside a running event loop (i.e. from an async
        context).  HttpSession._ensure_client() calls this, so the lock is
        always ready before any request is dispatched.
        """
        if self._lock is None:
            self._lock = asyncio.Lock()

    def _get_lock(self) -> asyncio.Lock:
        # Should never be None when called from request paths because
        # _ensure_client() calls ensure_lock() first, but guard anyway.
        if self._lock is None:  # pragma: no cover
            self._lock = asyncio.Lock()
        return self._lock

    def record_request(self, num_procedures: int = 1) -> None:
        """Record that an HTTP request was made carrying N procedures."""
        self.total_http_requests += 1
        self.total_procedures += num_procedures

    def update(self, headers: httpx.Headers) -> None:
        """Parse and store the rate-limit values from a response's headers."""
        raw_limit = headers.get("ratelimit-limit")
        raw_remaining = headers.get("ratelimit-remaining")
        raw_reset = headers.get("ratelimit-reset")

        if raw_limit is not None:
            with contextlib.suppress(ValueError):
                self.limit = int(raw_limit)

        if raw_remaining is not None:
            with contextlib.suppress(ValueError):
                new_remaining = int(raw_remaining)
                if self._prev_remaining is None or new_remaining > self._prev_remaining:
                    self.window_refreshes += 1
                    self._prev_remaining = new_remaining
                    self.remaining = new_remaining
                else:
                    self.remaining = min(self.remaining or new_remaining, new_remaining)
                    self._prev_remaining = self.remaining

        if raw_reset is not None:
            with contextlib.suppress(ValueError):
                self._reset_at = time.monotonic() + float(raw_reset)

    @property
    def quota_used_current_window(self) -> int | None:
        """Requests consumed in the current window (from headers)."""
        if self.limit is not None and self.remaining is not None:
            return self.limit - self.remaining
        return None

    async def wait_if_exhausted(self) -> None:
        """
        If the current window is exhausted (remaining == 0) sleep until
        the window resets, then reset our internal state so subsequent
        requests proceed normally.

        Uses a double-checked pattern: the condition is tested before
        acquiring the lock (fast path — no contention when quota is
        healthy) and again after acquiring it (slow path — ensures that
        only the *first* coroutine in a concurrent group actually sleeps;
        coroutines that queued behind the lock re-check and find
        ``remaining`` already reset to ``None``, so they skip the sleep
        and proceed immediately).
        """
        # Fast path: quota is healthy or not yet known — skip lock entirely.
        if self.remaining is None or self.remaining > 0:
            return

        async with self._get_lock():
            # Re-check after acquiring the lock.  The coroutine that got
            # here first will sleep and then null out remaining/reset_at.
            # Every subsequent waiter will find remaining == None and exit
            # without sleeping again.
            if self.remaining is not None and self.remaining <= 0 and self._reset_at is not None:
                wait_secs = self._reset_at - time.monotonic()
                if wait_secs > 0:
                    jitter = random.uniform(0.01, 0.5)
                    self.total_wait_seconds += wait_secs + jitter
                    logger.warning(
                        f"Rate limit exhausted. Sleeping for {wait_secs:.2f}s + {jitter:.2f}s jitter..."
                    )
                    await asyncio.sleep(wait_secs + jitter)
                # Reset state — next response will give us fresh values.
                self.remaining = None
                self._prev_remaining = None
                self._reset_at = None


class HttpSession:
    """
    Manages an httpx.AsyncClient with auth injection, header-based rate-limit
    throttling, and retry logic.

    Not intended for direct use — accessed through WareraClient.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
        initial_delay_ms: int = 250,
        max_delay_ms: int = 5000,
        backoff_multiplier: float = 2.0,
        jitter: bool = True,
        auto_batch_delay: float = 0.005,
        event_hooks: dict[str, list[Any]] | None = None,
        headers: dict[str, str] | None = None,
        retryable_status_codes: set[int] | list[int] | tuple[int, ...] | None = None,
        on_retry: OnRetryCallback | None = None,
    ) -> None:
        # Resolve API key: explicit arg > env var > None
        self._api_key: str | None = api_key or os.environ.get(_ENV_KEY)
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._initial_delay = initial_delay_ms / 1000.0
        self._max_delay = max_delay_ms / 1000.0
        self._backoff_multiplier = backoff_multiplier
        self._jitter = jitter
        self._client: httpx.AsyncClient | None = None
        self._rate_limit = _RateLimitState()
        self._auto_batch_queue: list[tuple[str, dict[str, Any], asyncio.Future[Any]]] = []
        self._auto_batch_task: asyncio.Task[None] | None = None
        self._auto_batch_delay = auto_batch_delay
        self._event_hooks = event_hooks or {}
        self._custom_headers = headers or {}
        self._on_retry = on_retry
        self._swr_cache = SWRCache()
        self._retryable_status_codes = frozenset(
            retryable_status_codes
            if retryable_status_codes is not None
            else {408, 409, 425, 429, 500, 502, 503, 504}
        )

    def _is_retryable(self, exc: BaseException) -> bool:
        """Retry on specific status codes and network errors."""
        if isinstance(exc, httpx.TransportError):
            return True
        if isinstance(exc, WareraHTTPError):
            return exc.status_code in self._retryable_status_codes
        return False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def __aenter__(self) -> HttpSession:
        await self._ensure_client()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.aclose()

    async def _ensure_client(self) -> None:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=self._timeout,
                headers={"User-Agent": "warera-client", "rt": _RT_HEADER, **self._custom_headers},
                follow_redirects=True,
                http2=True,
                limits=httpx.Limits(max_connections=200, max_keepalive_connections=50),
                event_hooks=self._event_hooks,
            )
        # Ensure the rate-limit lock is created inside the running event loop.
        # This is safe to call repeatedly — it is a no-op after the first call.
        self._rate_limit.ensure_lock()

    async def aclose(self) -> None:
        if self._auto_batch_task and not self._auto_batch_task.done():
            self._auto_batch_task.cancel()
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    # ------------------------------------------------------------------
    # Auth helpers
    # ------------------------------------------------------------------

    def _auth_headers(self) -> dict[str, str]:
        if self._api_key:
            return {"X-API-Key": self._api_key}
        return {}

    # ------------------------------------------------------------------
    # Retry helper — built at call time so max_retries / backoff_multiplier /
    # jitter are actually honoured instead of being silently ignored by a
    # static @retry decorator with hardcoded values.
    # ------------------------------------------------------------------

    def _make_before_sleep(self) -> Callable[[Any], None]:
        """
        Build the tenacity ``before_sleep`` hook: always debug-log the retry,
        and additionally invoke the user's ``on_retry`` callback when set.
        """
        log_cb = before_sleep_log(logger, logging.DEBUG)
        on_retry = self._on_retry
        if on_retry is None:
            return log_cb

        def combined(retry_state: Any) -> None:
            log_cb(retry_state)
            exc = retry_state.outcome.exception() if retry_state.outcome else None
            delay = float(retry_state.next_action.sleep) if retry_state.next_action else 0.0
            info = RetryInfo(
                attempt=retry_state.attempt_number,
                delay_s=delay,
                error=exc,
                status_code=getattr(exc, "status_code", None),
            )
            try:
                on_retry(info)
            except Exception:
                # A user callback must never break the retry loop itself.
                logger.exception("on_retry callback raised; ignoring")

        return combined

    def _retrying(self) -> AsyncRetrying:
        """Return a new AsyncRetrying instance configured from this session's params."""
        wait_cls = wait_random_exponential if self._jitter else wait_exponential
        return AsyncRetrying(
            retry=retry_if_exception(self._is_retryable),
            stop=stop_after_attempt(self._max_retries + 1),
            wait=wait_cls(
                multiplier=self._initial_delay,
                exp_base=self._backoff_multiplier,
                max=self._max_delay,
            ),
            before_sleep=self._make_before_sleep(),
            reraise=True,
        )

    # ------------------------------------------------------------------
    # Single call  →  GET /procedure?input=<json>
    # ------------------------------------------------------------------

    async def get(self, procedure: str, params: dict[str, Any]) -> Any:
        """
        Execute a single tRPC GET call.
        Automatically intercepts and bundles concurrent calls into a single batch POST
        to drastically reduce network overhead and rate limit consumption.
        """
        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        self._auto_batch_queue.append((procedure, params, fut))
        logger.debug(
            f"Queuing '{procedure}' for auto-batching (queue size: {len(self._auto_batch_queue)})"
        )

        if self._auto_batch_task is None:
            self._auto_batch_task = loop.create_task(self._auto_batch_flush())

        return await fut

    async def get_swr(self, procedure: str, params: dict[str, Any], ttl_seconds: float) -> Any:
        """
        Execute a GET call wrapped in an SWR cache.
        Returns stale data instantly if available, while fetching fresh data in the background.
        """
        # Create a deterministic cache key
        key_dict = {"p": procedure, "args": params}
        if _orjson is not None:
            key = _orjson.dumps(key_dict, option=_orjson.OPT_SORT_KEYS).decode("utf-8")
        else:
            key = json.dumps(key_dict, sort_keys=True)

        async def fetcher() -> Any:
            return await self.get(procedure, params)

        return await self._swr_cache.get(key, ttl_seconds, fetcher)

    async def _auto_batch_flush(self) -> None:
        # Wait a brief moment to let other concurrent event-loop tasks queue up.
        await asyncio.sleep(self._auto_batch_delay)

        queue = self._auto_batch_queue
        self._auto_batch_queue = []
        self._auto_batch_task = None

        if not queue:
            return

        logger.debug(f"Flushing batch of {len(queue)} procedures...")

        if len(queue) == 1:
            proc, params, fut = queue[0]
            try:
                res = await self._real_get(proc, params)
                if not fut.done():
                    fut.set_result(res)
            except BaseException as e:
                if not fut.done():
                    fut.set_exception(e)
                if isinstance(e, asyncio.CancelledError):
                    raise
            return

        for start_idx in range(0, len(queue), 50):
            chunk = queue[start_idx : start_idx + 50]
            procedures = [q[0] for q in chunk]
            inputs = [q[1] for q in chunk]
            futs = [q[2] for q in chunk]
    
            try:
                results = await self.post_batch(procedures, inputs)
                for fut, res in zip(futs, results, strict=True):
                    if not fut.done():
                        fut.set_result(res)
            except WareraBatchError as exc:
                for i, fut in enumerate(futs):
                    if fut.done():
                        continue
                    if i in exc.errors:
                        fut.set_exception(exc.errors[i])
                    else:
                        fut.set_result(exc.results.get(i))
            except BaseException as e:
                for fut in futs:
                    if not fut.done():
                        fut.set_exception(e)
                if isinstance(e, asyncio.CancelledError):
                    raise

    async def _real_get(self, procedure: str, params: dict[str, Any]) -> Any:
        await self._ensure_client()

        clean = {k: v for k, v in params.items() if v is not None}
        if _orjson is not None:
            encoded = quote(_orjson.dumps(clean).decode("utf-8"), safe="")
        else:
            encoded = quote(json.dumps(clean, separators=(",", ":")), safe="")
        url = f"/{procedure}?input={encoded}"

        response = await self._get_with_retry(url)
        return self._unwrap_single(response, procedure)

    async def _get_with_retry(self, url: str) -> httpx.Response:
        result: httpx.Response | None = None
        async for attempt in self._retrying():
            with attempt:
                # Respect the server-reported rate-limit window before sending.
                await self._rate_limit.wait_if_exhausted()
                if self._client is None:
                    raise RuntimeError("HTTP client is not initialised — call __aenter__ first")
                resp = await self._client.get(url, headers=self._auth_headers())
                # Update rate-limit state from response headers.
                self._rate_limit.update(resp.headers)
                self._rate_limit.record_request(num_procedures=1)
                self._check_response(resp)
                result = resp
        return result  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # Batch call  →  POST /proc0,proc1,...?batch=1   body: {"0": {}, ...}
    # ------------------------------------------------------------------

    async def post_batch(
        self,
        procedures: list[str],
        inputs: list[dict[str, Any]],
        *,
        chunk_size: int = 50,
    ) -> list[Any]:
        """
        Execute one or more tRPC batch POSTs, automatically splitting oversized
        lists into chunks of at most ``chunk_size`` (hard-capped at 50, the
        server's enforced limit).

        Returns a list of parsed ``result.data`` values in the same order as
        ``procedures``.  Raises :exc:`WareraBatchError` if any item fails.

        Args:
            procedures: Procedure names to call, e.g. ``["company.getById", ...]``.
            inputs:     Corresponding input dicts, one per procedure.
            chunk_size: Max procedures per physical HTTP request.  Values above
                        the server hard limit of 50 are clamped silently.
        """
        await self._ensure_client()

        if not procedures:
            return []

        # Strip None values from all inputs (consistency with GET requests)
        clean_inputs = [{k: v for k, v in inp.items() if v is not None} for inp in inputs]

        # Clamp to the server hard limit regardless of what was passed.
        _MAX_BATCH = 50
        effective = min(max(1, chunk_size), _MAX_BATCH)

        # Fast path: fits in one request.
        if len(procedures) <= effective:
            proc_path = ",".join(procedures)
            url = f"/{proc_path}?batch=1"
            body = {str(i): inp for i, inp in enumerate(clean_inputs)}
            raw_list = await self._post_batch_with_retry(url, body)
            return self._unwrap_batch(raw_list, procedures)

        # Slow path: split into chunks and collect results in order.
        # Chunks are fired concurrently — the header-based rate-limit tracker
        # will sleep automatically if the window is exhausted mid-flight.
        chunks: list[tuple[list[str], list[dict[str, Any]]]] = []
        for start in range(0, len(procedures), effective):
            end = start + effective
            chunks.append((procedures[start:end], clean_inputs[start:end]))

        async def _run_chunk(procs: list[str], inps: list[dict[str, Any]]) -> list[Any]:
            proc_path = ",".join(procs)
            url = f"/{proc_path}?batch=1"
            body = {str(i): inp for i, inp in enumerate(inps)}
            raw = await self._post_batch_with_retry(url, body)
            return self._unwrap_batch(raw, procs)

        chunk_results = await asyncio.gather(*[_run_chunk(p, i) for p, i in chunks])
        return [item for sublist in chunk_results for item in sublist]

    async def _post_batch_with_retry(self, url: str, body: dict[str, Any]) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] | None = None
        async for attempt in self._retrying():
            with attempt:
                # Respect the server-reported rate-limit window before sending.
                await self._rate_limit.wait_if_exhausted()
                if self._client is None:
                    raise RuntimeError("HTTP client is not initialised — call __aenter__ first")
                headers = {**self._auth_headers(), "Content-Type": "application/json"}
                if _orjson is not None:
                    content = _orjson.dumps(body)
                    resp = await self._client.post(url, content=content, headers=headers)
                else:
                    resp = await self._client.post(url, json=body, headers=headers)
                # Update rate-limit state from response headers.
                self._rate_limit.update(resp.headers)
                self._rate_limit.record_request(num_procedures=len(body))
                self._check_response(resp)
                data = _orjson.loads(resp.content) if _orjson is not None else resp.json()
                if not isinstance(data, list):
                    raise ValueError(
                        f"Expected list from batch endpoint, got {type(data).__name__}"
                    )
                result = data
        return result  # type: ignore[return-value]

    # ------------------------------------------------------------------
    # Response parsing helpers
    # ------------------------------------------------------------------

    def _check_response(self, resp: httpx.Response) -> None:
        """Raise the appropriate WareraHTTPError for non-2xx responses."""
        if resp.status_code < 400:
            return

        # Surface the Retry-After header value when rate-limited so callers
        # can respect it without having to inspect the raw response themselves.
        if resp.status_code == 429:
            retry_after: float | None = None
            raw_header = resp.headers.get("Retry-After")
            if raw_header is not None:
                with contextlib.suppress(ValueError):
                    retry_after = float(raw_header)
            try:
                body = _orjson.loads(resp.content) if _orjson is not None else resp.json()
            except Exception:
                body = resp.text
            raise WareraRateLimitError(retry_after=retry_after, response_body=body)

        try:
            body = _orjson.loads(resp.content) if _orjson is not None else resp.json()
        except Exception:
            body = resp.text
        _raise_for_status(resp.status_code, body, api_key_configured=bool(self._api_key))

    def _unwrap_single(self, resp: httpx.Response, procedure: str) -> Any:
        """
        tRPC single response shape:
          { "result": { "data": <payload> } }
        or an error:
          { "error": { "message": "...", "code": ... } }
        """
        try:
            data = _orjson.loads(resp.content) if _orjson is not None else resp.json()
        except Exception as exc:
            raise ValueError(f"Non-JSON response from {procedure}: {resp.text}") from exc

        if "error" in data:
            err = data["error"]
            code = err.get("data", {}).get("httpStatus", 500)
            _raise_for_status(code, err, api_key_configured=bool(self._api_key))

        try:
            return data["result"]["data"]
        except (KeyError, TypeError) as exc:
            raise ValueError(f"Unexpected tRPC response shape from {procedure}: {data}") from exc

    def _unwrap_batch(self, raw_list: list[dict[str, Any]], procedures: list[str]) -> list[Any]:
        """
        tRPC batch response shape:
          [
            { "result": { "data": <payload> } },   ← success
            { "error": { "message": "...", ... } }, ← failure
            ...
          ]

        Returns a list of unwrapped data values.
        Raises WareraBatchError if any item errored.
        """
        results: dict[int, Any] = {}
        errors: dict[int, WareraError] = {}

        for i, (item, proc) in enumerate(zip(raw_list, procedures, strict=True)):
            if "error" in item:
                err = item["error"]
                code = err.get("data", {}).get("httpStatus", 500)
                try:
                    _raise_for_status(code, err, api_key_configured=bool(self._api_key))
                except WareraHTTPError as e:
                    errors[i] = e
            else:
                try:
                    results[i] = item["result"]["data"]
                except (KeyError, TypeError):
                    errors[i] = WareraValidationError(
                        f"Bad shape at batch index {i} ({proc}): {item}", item
                    )

        if errors:
            raise WareraBatchError(errors=errors, results=results)

        return [results[i] for i in range(len(procedures))]
