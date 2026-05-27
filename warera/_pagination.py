"""
Pagination helpers for cursor-based WarEra API endpoints.

Provides the `auto_paginate_pages` engine that powers `auto_paginate=True`.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator, Callable, Coroutine
from datetime import datetime
from typing import Any, TypeVar

from .models.common import CursorPage

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


async def auto_paginate_pages(
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
