from __future__ import annotations

import asyncio
import contextlib
import os
from collections.abc import AsyncGenerator, Callable, Coroutine
from datetime import datetime, timedelta, timezone
from typing import Any, TypeVar

from .models.common import CursorPage

"""
Pagination helpers for cursor-based WarEra API endpoints.

Provides the `_auto_paginate_pages` engine that powers `auto_items=True` and `collect_all`.
"""


T = TypeVar("T")

# A callable that accepts keyword args including an optional `cursor` and
# returns a coroutine that resolves to a CursorPage[T].
PageFetcher = Callable[..., Coroutine[Any, Any, CursorPage[T]]]


def _parse_cursor_date(cursor: str) -> datetime | None:
    """Extracts and parses the datetime portion of a '{iso_date}|{id}' cursor."""
    if not cursor or "|" not in cursor:
        return None
    date_str = cursor.split("|", 1)[0]

    # Handle JS Date format: "Wed May 27 2026 05:41:00 GMT+0000 (Coordinated Universal Time)"
    if "GMT" in date_str:
        try:
            from datetime import timezone

            clean_str = date_str[:24]
            dt = datetime.strptime(clean_str, "%a %b %d %Y %H:%M:%S")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    try:
        # e.g., "2026-05-27T03:04:15Z" -> Python datetime
        date_str = date_str.replace("Z", "+00:00")
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None


async def _auto_paginate_pages(
    fetch_fn: PageFetcher[T],
    max_pages: int | float = float("inf"),
    cursor_end: datetime | str | None = None,
    **kwargs: Any,
) -> AsyncGenerator[CursorPage[T], None]:
    """
    Async generator that fetches and yields full CursorPages transparently.
    Stops when has_more=False, max_pages is reached, or cursor_end is hit.

    Args:
        fetch_fn:   An async callable returning a CursorPage[T].
        max_pages:  Max number of pages to yield.
        cursor_end: Cutoff date. Stops when the next_cursor is older than this.
        **kwargs:   Extra arguments forwarded to the fetch_fn.
    """
    if isinstance(cursor_end, str):
        cursor_end = cursor_end.replace("Z", "+00:00")
        cursor_end = datetime.fromisoformat(cursor_end)

    # If the user supplied an initial cursor (e.g., from `get_paginated(cursor="foo")`), use it.
    cursor: str | None = kwargs.pop("cursor", None)
    pages_fetched = 0

    while pages_fetched < max_pages:
        page: CursorPage[T] = await fetch_fn(**kwargs, cursor=cursor)
        yield page
        pages_fetched += 1

        if not page.has_more or not page.next_cursor:
            break

        # Check cursor_end cutoff
        if cursor_end is not None:
            c_date = _parse_cursor_date(page.next_cursor)
            # If the cursor date is strictly older than cursor_end, we stop
            if c_date is not None and c_date < cursor_end:
                break

        cursor = page.next_cursor


async def auto_paginate_items(
    fetch_fn: PageFetcher[T],
    max_pages: int | float = float("inf"),
    cursor_end: datetime | str | None = None,
    **kwargs: Any,
) -> AsyncGenerator[T, None]:
    """
    Async generator that fetches pages transparently and yields individual items directly.
    """
    async for page in _auto_paginate_pages(
        fetch_fn, max_pages=max_pages, cursor_end=cursor_end, **kwargs
    ):
        for item in page.items:
            yield item


WARERA_EPOCH = datetime(2025, 1, 1, tzinfo=timezone.utc)
WARERA_MAX_CONCURRENCY = int(os.environ.get("WARERA_MAX_CONCURRENCY", 500))


async def parallel_collect_all(
    fetch_fn: Callable[
        ..., Coroutine[Any, Any, CursorPage[T]]
    ],
    oldest_date: datetime | str | None = None,
    time_slice_days: float = 0.2,
    concurrency: int | None = None,
    **kwargs: Any,
) -> list[T]:
    """
    Generic parallel time-slicing engine to fetch paginated resources concurrently.
    Automatically generates chunks of `time_slice_days` from `now` backward to `oldest_date`.
    """
    if oldest_date is None:
        oldest_date = WARERA_EPOCH
    elif isinstance(oldest_date, str):
        oldest_date = datetime.fromisoformat(oldest_date.replace("Z", "+00:00"))

    now = datetime.now(timezone.utc)
    chunks: list[tuple[str | None, datetime]] = []
    current_end = now

    while current_end > oldest_date:
        chunk_start = max(oldest_date, current_end - timedelta(days=time_slice_days))

        if current_end == now:
            cursor = None
        else:
            iso_str = current_end.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            cursor = f"{iso_str}|000000000000000000000000"

        chunks.append((cursor, chunk_start))
        current_end = chunk_start

    concurrency = concurrency or WARERA_MAX_CONCURRENCY
    sem = asyncio.Semaphore(concurrency)
    abort_event = asyncio.Event()

    async def fetch_chunk(cur: str | None, cur_end: datetime) -> list[T]:
        if abort_event.is_set():
            return []

        chunk_items: list[T] = []
        async with sem:
            if abort_event.is_set():
                return []

            result = _auto_paginate_pages(
                fetch_fn, cursor=cur, cursor_end=cur_end.isoformat(), **kwargs
            )
            async for page in result:
                chunk_items.extend(page.items)
                if not getattr(page, "has_more", True):
                    abort_event.set()
        return chunk_items

    chunk_results = await asyncio.gather(*[fetch_chunk(c, start) for c, start in chunks])

    unique_items: list[T] = []
    seen = set()

    for chunk in chunk_results:
        for item in chunk:
            # Pydantic models usually have .id or fallback to hashing?
            # In this API, almost everything has an ID.
            item_id = getattr(item, "id", None)
            if item_id is None:
                # Can not reliably deduplicate, just append
                unique_items.append(item)
                continue

            if item_id not in seen:
                seen.add(item_id)
                unique_items.append(item)

    # Attempt to sort globally by descending created_at
    with contextlib.suppress(Exception):
        unique_items.sort(
            key=lambda x: getattr(x, "created_at", getattr(x, "createdAt", "")), reverse=True
        )

    return unique_items
