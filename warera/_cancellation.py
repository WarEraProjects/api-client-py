from __future__ import annotations

import asyncio
import contextvars
import threading
from typing import Any

_cancellation_scope_var: contextvars.ContextVar[CancellationScope | None] = contextvars.ContextVar(
    "cancellation_scope", default=None
)


class CancellationScope:
    """
    A context manager for cancelling pending requests, analogous to JS AbortController.

    Any API requests made inside the `with` block (both sync and async) will be
    registered with this scope. Calling `.cancel()` from another thread or task
    will instantly abort all registered pending HTTP requests.
    """

    def __init__(self) -> None:
        self.is_cancelled: bool = False
        self._tasks: set[asyncio.Task[Any]] = set()
        self._tokens: list[contextvars.Token[CancellationScope | None]] = []
        self._lock = threading.Lock()

    def __enter__(self) -> CancellationScope:
        token = _cancellation_scope_var.set(self)
        with self._lock:
            self._tokens.append(token)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        with self._lock:
            token = self._tokens.pop() if self._tokens else None
        if token:
            _cancellation_scope_var.reset(token)

    async def __aenter__(self) -> CancellationScope:
        return self.__enter__()

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.__exit__(exc_type, exc_val, exc_tb)

    def cancel(self) -> None:
        """Cancel all pending requests registered in this scope."""
        with self._lock:
            self.is_cancelled = True
            tasks = list(self._tasks)

        for task in tasks:
            if not task.done():
                try:
                    loop = task.get_loop()
                    loop.call_soon_threadsafe(task.cancel)
                except Exception:
                    pass

    def _register(self, task: asyncio.Task[Any]) -> None:
        with self._lock:
            self._tasks.add(task)
            should_cancel = self.is_cancelled

        if should_cancel and not task.done():
            task.get_loop().call_soon_threadsafe(task.cancel)

    def _unregister(self, task: asyncio.Task[Any]) -> None:
        with self._lock:
            self._tasks.discard(task)


def get_current_scope() -> CancellationScope | None:
    """Return the active cancellation scope, if any."""
    return _cancellation_scope_var.get()
