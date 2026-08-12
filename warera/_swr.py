from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable, Coroutine
from typing import Any, TypeVar, cast

from .cache_backends import CacheBackend, MemoryCacheBackend
from .telemetry import TelemetryHooks

logger = logging.getLogger("warera.swr")

T = TypeVar("T")


class SWRCache:
    """
    A simple Stale-While-Revalidate (SWR) cache engine.
    """

    def __init__(
        self,
        backend: CacheBackend | None = None,
        telemetry: TelemetryHooks | None = None,
    ) -> None:
        self._cache = backend or MemoryCacheBackend()
        self._telemetry = telemetry
        # Tracks keys currently being revalidated to avoid duplicate concurrent requests
        self._inflight: dict[str, asyncio.Task[Any]] = {}

    async def get(
        self, key: str, ttl_seconds: float, fetcher: Callable[[], Coroutine[Any, Any, T]]
    ) -> T:
        """
        Get a value from the cache using SWR semantics.

        - If the key is not in cache, fetch immediately, block, and return.
        - If the key is in cache and fresh, return instantly.
        - If the key is in cache but stale, return instantly and fire a background task to update it.
        """
        now = time.time()
        cached = self._cache.get(key)

        if cached is not None:
            data, fetch_time = cached
            is_stale = now - fetch_time > ttl_seconds

            if self._telemetry:
                self._telemetry.on_cache_hit(key, is_stale)

            if is_stale:
                logger.debug(
                    f"SWR Cache hit (stale) for '{key}'. Triggering background revalidation."
                )
                self._revalidate(key, fetcher)
            else:
                logger.debug(f"SWR Cache hit (fresh) for '{key}'.")
            return cast(T, data)

        # Not in cache, must block and fetch
        if key in self._inflight:
            logger.debug(f"SWR Cache miss for '{key}'. Awaiting existing inflight fetch.")
            return cast(T, await self._inflight[key])

        logger.debug(f"SWR Cache miss for '{key}'. Fetching data synchronously.")
        return await self._do_fetch(key, fetcher)

    def _revalidate(self, key: str, fetcher: Callable[[], Coroutine[Any, Any, T]]) -> None:
        """Launch a background task to update the cache if one isn't already running."""
        if key in self._inflight:
            return

        loop = asyncio.get_running_loop()
        task = loop.create_task(self._do_fetch(key, fetcher))
        self._inflight[key] = task

        def _log_exc(t: asyncio.Task[T]) -> None:
            if not t.cancelled() and t.exception():
                logger.warning(f"Background revalidation failed for '{key}': {t.exception()}")

        task.add_done_callback(_log_exc)

    async def _do_fetch(self, key: str, fetcher: Callable[[], Coroutine[Any, Any, T]]) -> T:
        """Execute the fetcher, store the result, and manage the inflight lock."""
        task: asyncio.Task[T] = asyncio.create_task(fetcher())
        self._inflight[key] = task

        def _on_done(t: asyncio.Task[T]) -> None:
            self._inflight.pop(key, None)
            if not t.cancelled() and not t.exception():
                self._cache.set(key, t.result(), time.time())
                if self._cache.get_size() > 1000:
                    self._cache.pop_oldest()

        task.add_done_callback(_on_done)
        return await task

    def clear(self) -> None:
        for task in self._inflight.values():
            task.cancel()
        """Clear the cache entirely."""
        self._cache.clear()
        self._inflight.clear()
