"""
Synchronous shim over WareraClient.

Every async method is wrapped so callers don't need asyncio boilerplate.
Useful for scripts, notebooks, and REPLs.

Usage:
    from warera.sync import WareraClient

    client = WareraClient(api_key="...")
    user    = client.user.get_by_id("12345")
    prices  = client.item_trading.get_prices()

    # Batch
    with client.batch() as batch:
        c1  = batch.add("company.getById", {"companyId": "111"})
        gov = batch.add("government.getByCountryId", {"countryId": "7"})
    print(c1.result)

Note: This module spawns a daemon thread with an isolated asyncio event loop
to safely run coroutines without interfering with the main thread's loop.
"""

from __future__ import annotations

import asyncio
import atexit
import functools
import inspect
import queue
import threading
from collections.abc import Iterator
from typing import Any, cast

from ._batch import BatchSession
from .client import WareraClient as _AsyncClient

# ---------------------------------------------------------------------------
# Background Event Loop Engine
# ---------------------------------------------------------------------------

_bg_loop: asyncio.AbstractEventLoop | None = None
_bg_thread: threading.Thread | None = None
_loop_lock = threading.Lock()


def _start_bg_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()


def _ensure_loop() -> asyncio.AbstractEventLoop:
    global _bg_loop, _bg_thread
    with _loop_lock:
        if _bg_loop is None:
            _bg_loop = asyncio.new_event_loop()
            _bg_thread = threading.Thread(
                target=_start_bg_loop, args=(_bg_loop,), daemon=True, name="WareraSyncThread"
            )
            _bg_thread.start()
        return _bg_loop


def shutdown() -> None:
    """Gracefully terminate the background asyncio event loop and thread."""
    global _bg_loop, _bg_thread
    with _loop_lock:
        if _bg_loop is not None and _bg_loop.is_running():
            _bg_loop.call_soon_threadsafe(_bg_loop.stop)
            if _bg_thread is not None:
                _bg_thread.join(timeout=2.0)
        _bg_loop = None
        _bg_thread = None

atexit.register(shutdown)


def _run(coro: Any) -> Any:
    """Run a coroutine synchronously on the background event loop."""
    loop = _ensure_loop()
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    return future.result()


def _run_async_gen(async_gen: Any) -> Iterator[Any]:
    """Drain an async generator into a thread-safe Queue and yield synchronously."""
    loop = _ensure_loop()
    q: queue.Queue[Any] = queue.Queue()
    _sentinel = object()
    stop_event = threading.Event()

    async def _producer() -> None:
        try:
            async for item in async_gen:
                if stop_event.is_set():
                    break

                # Backpressure: wait if the queue is getting large so we don't blow out memory
                # Check periodically to ensure we notice stop_event
                while q.qsize() > 50:
                    await asyncio.sleep(0.05)
                    if stop_event.is_set():
                        break

                if stop_event.is_set():
                    break

                q.put((True, item))
        except Exception as e:
            q.put((False, e))
        finally:
            q.put(_sentinel)

    task = asyncio.run_coroutine_threadsafe(_producer(), loop)

    try:
        while True:
            msg = q.get()
            if msg is _sentinel:
                break
            ok, val = msg
            if not ok:
                raise val
            yield val
    finally:
        stop_event.set()
        loop.call_soon_threadsafe(task.cancel)


def _sync_generator(async_gen_fn: Any, *args: Any, **kwargs: Any) -> Iterator[Any]:
    """Helper to call an async generator function and consume it synchronously."""
    return _run_async_gen(async_gen_fn(*args, **kwargs))


# ---------------------------------------------------------------------------
# Synchronous Wrappers
# ---------------------------------------------------------------------------


def _wrap_resource(async_resource: Any) -> _SyncResourceProxy:
    return _SyncResourceProxy(async_resource)


class _SyncResourceProxy:
    """
    Wraps an async resource class, making every coroutine method callable
    synchronously and every async generator method return a true generator.
    """

    def __init__(self, resource: Any) -> None:
        self._resource = resource

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._resource, name)

        if inspect.iscoroutinefunction(attr):

            @functools.wraps(attr)
            def sync_method(*args: Any, **kwargs: Any) -> Any:
                result = _run(attr(*args, **kwargs))
                # In rare cases where a coroutine returns an async generator
                if inspect.isasyncgen(result):
                    return _run_async_gen(result)
                return result

            return sync_method

        if inspect.isasyncgenfunction(attr):

            @functools.wraps(attr)
            def sync_gen(*args: Any, **kwargs: Any) -> Any:
                yield from _sync_generator(attr, *args, **kwargs)

            return sync_gen

        # Check if the attr itself is a callable that returns an asyncgen,
        # but isn't strictly an asyncgen function (e.g. decorators)
        if callable(attr):

            @functools.wraps(attr)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                res = attr(*args, **kwargs)
                if inspect.isasyncgen(res):
                    yield from _run_async_gen(res)
                elif inspect.iscoroutine(res):
                    ret = _run(res)
                    if inspect.isasyncgen(ret):
                        yield from _run_async_gen(ret)
                    else:
                        return ret
                else:
                    return res

            return wrapper

        return attr


class _SyncBatchSession:
    """Synchronous wrapper around BatchSession."""

    def __init__(self, session: BatchSession) -> None:
        self._session = session

    def add(self, procedure: str, input_: dict[str, Any] | None = None) -> Any:
        return self._session.add(procedure, input_)

    def __enter__(self) -> _SyncBatchSession:
        return self

    def __exit__(self, *_: Any) -> None:
        _run(self._session.flush())


class WareraClient:
    """
    Synchronous WarEra API client.

    Wraps the async WareraClient — every method is callable without await.
    Constructor arguments are identical to the async client.
    """

    def __init__(self, api_key: str | None = None, **kwargs: Any) -> None:
        self._async_client = _AsyncClient(api_key=api_key, **kwargs)
        _run(self._async_client._http.__aenter__())
    def __del__(self) -> None:
        import contextlib
        with contextlib.suppress(Exception):
            self.close()

        # Wrap every resource namespace
        self.alliance = _wrap_resource(self._async_client.alliance)
        self.user = _wrap_resource(self._async_client.user)
        self.company = _wrap_resource(self._async_client.company)
        self.country = _wrap_resource(self._async_client.country)
        self.government = _wrap_resource(self._async_client.government)
        self.region = _wrap_resource(self._async_client.region)
        self.battle = _wrap_resource(self._async_client.battle)
        self.battle_loot_summary = _wrap_resource(self._async_client.battle_loot_summary)
        self.battle_ranking = _wrap_resource(self._async_client.battle_ranking)
        self.battle_order = _wrap_resource(self._async_client.battle_order)
        self.round = _wrap_resource(self._async_client.round)
        self.event = _wrap_resource(self._async_client.event)
        self.item_trading = _wrap_resource(self._async_client.item_trading)
        self.work_offer = _wrap_resource(self._async_client.work_offer)
        self.worker = _wrap_resource(self._async_client.worker)
        self.work = _wrap_resource(self._async_client.work)
        self.mercenary_contract_auction = _wrap_resource(
            self._async_client.mercenary_contract_auction
        )
        self.mu = _wrap_resource(self._async_client.mu)
        self.mu_member = _wrap_resource(self._async_client.mu_member)
        self.party = _wrap_resource(self._async_client.party)
        self.donation = _wrap_resource(self._async_client.donation)
        self.election = _wrap_resource(self._async_client.election)
        self.game_stat = _wrap_resource(self._async_client.game_stat)
        self.ranking = _wrap_resource(self._async_client.ranking)
        self.transaction = _wrap_resource(self._async_client.transaction)
        self.upgrade = _wrap_resource(self._async_client.upgrade)
        self.article = _wrap_resource(self._async_client.article)
        self.search = _wrap_resource(self._async_client.search)
        self.game_config = _wrap_resource(self._async_client.game_config)
        self.inventory = _wrap_resource(self._async_client.inventory)
        self.action_log = _wrap_resource(self._async_client.action_log)
        self.tournament = _wrap_resource(self._async_client.tournament)

    def batch(
        self, batch_size: int | None = None, concurrency: int | None = None
    ) -> _SyncBatchSession:
        return _SyncBatchSession(self._async_client.batch(batch_size, concurrency))

    @property
    def has_api_key(self) -> bool:
        """Whether an API key is configured on this client."""
        return self._async_client.has_api_key

    def validate_api_key(self) -> bool:
        """
        Check whether the configured API key is accepted by the server.
        Returns False when no key is configured or the server rejects it (401).
        """
        return cast(bool, _run(self._async_client.validate_api_key()))

    def close(self) -> None:
        _run(self._async_client.aclose())

    def __enter__(self) -> WareraClient:
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return repr(self._async_client).replace("WareraClient", "sync.WareraClient")


_default_client: WareraClient | None = None
api_key: str | None = None


def set_api_key(key: str, *, validate: bool = False) -> None:
    """
    Configure the global API key for the module-level sync client.

    Args:
        key:      The X-API-Key value.
        validate: When True, immediately test the key against the server and
                  raise :class:`warera.WareraUnauthorizedError` if rejected.
    """
    global api_key, _default_client
    api_key = key
    if _default_client is not None:
        _default_client._async_client._http._api_key = key
    if validate and not get_client().validate_api_key():
        from .exceptions import WareraUnauthorizedError

        raise WareraUnauthorizedError(api_key_configured=True)


def validate_api_key() -> bool:
    """Check whether the configured API key is accepted by the server."""
    return get_client().validate_api_key()


def get_client() -> WareraClient:
    """Get or create the global synchronous WareraClient."""
    global _default_client
    if _default_client is None:
        _default_client = WareraClient(api_key=api_key)
    return _default_client


_RESOURCE_NAMES = {
    "action_log",
    "alliance",
    "article",
    "battle",
    "battle_loot_summary",
    "battle_order",
    "battle_ranking",
    "company",
    "country",
    "donation",
    "election",
    "event",
    "game_config",
    "game_stat",
    "government",
    "inventory",
    "item_trading",
    "mercenary_contract_auction",
    "mu",
    "mu_member",
    "party",
    "ranking",
    "region",
    "round",
    "search",
    "tournament",
    "transaction",
    "upgrade",
    "user",
    "work",
    "work_offer",
    "worker",
}


def __getattr__(name: str) -> Any:
    if name in _RESOURCE_NAMES:
        return getattr(get_client(), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
