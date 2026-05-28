from __future__ import annotations

import asyncio
import time
from collections.abc import Callable, Coroutine
from typing import Any, TypeVar, cast

T = TypeVar("T")


class SWRCache:
    """
    A simple Stale-While-Revalidate (SWR) cache engine.
    """

    def __init__(self) -> None:
        # Maps key -> (data, fetch_timestamp)
        self._cache: dict[str, tuple[Any, float]] = {}
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

        if key in self._cache:
            data, fetch_time = self._cache[key]
            if now - fetch_time > ttl_seconds:
                self._revalidate(key, fetcher)
            return cast(T, data)

        # Not in cache, must block and fetch
        if key in self._inflight:
            return cast(T, await self._inflight[key])

        return await self._do_fetch(key, fetcher)

    def _revalidate(self, key: str, fetcher: Callable[[], Coroutine[Any, Any, T]]) -> None:
        """Launch a background task to update the cache if one isn't already running."""
        if key in self._inflight:
            return

        loop = asyncio.get_running_loop()
        # Fire and forget the background task
        loop.create_task(self._do_fetch(key, fetcher))

    async def _do_fetch(self, key: str, fetcher: Callable[[], Coroutine[Any, Any, T]]) -> T:
        """Execute the fetcher, store the result, and manage the inflight lock."""
        task: asyncio.Task[T] = asyncio.create_task(fetcher())
        self._inflight[key] = task
        try:
            data = await task
            self._cache[key] = (data, time.time())
            return data
        finally:
            self._inflight.pop(key, None)

    def clear(self) -> None:
        """Clear the cache entirely."""
        self._cache.clear()
        self._inflight.clear()
