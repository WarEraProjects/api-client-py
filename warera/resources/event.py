from __future__ import annotations

import typing
from collections.abc import AsyncIterator

from .._enums import EventType
from .._pagination import auto_paginate_pages
from ..models.common import CursorPage
from ..models.event import Event
from ._base import BaseResource


class EventResource(BaseResource):
    """
    Endpoints:
      • event.getEventsPaginated  (cursor-paginated)
    """

    @typing.overload
    async def get_paginated(
        self,
        *,
        limit: int = 10,
        cursor: str | None = None,
        country_id: str | None = None,
        event_types: list[EventType | str] | None = None,
        auto_paginate: typing.Literal[False] = False,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Event]: ...

    @typing.overload
    async def get_paginated(
        self,
        *,
        limit: int = 10,
        cursor: str | None = None,
        country_id: str | None = None,
        event_types: list[EventType | str] | None = None,
        auto_paginate: typing.Literal[True],
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[CursorPage[Event]]: ...

    async def get_paginated(
        self,
        *,
        limit: int = 10,
        cursor: str | None = None,
        country_id: str | None = None,
        event_types: list[EventType | str] | None = None,
        auto_paginate: bool = False,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Event] | AsyncIterator[CursorPage[Event]] | AsyncIterator[Event]:
        """Get game events, optionally filtered by country and/or event type."""
        if auto_items:
            from .._pagination import auto_paginate_items
            return auto_paginate_items(
                self.get_paginated,
                max_pages=max_pages,
                cursor_end=cursor_end,
                **{k: v for k, v in locals().items() if k not in ("self", "auto_paginate", "auto_items", "max_pages", "cursor_end", "kwargs")}
            )
        if auto_items:
            from .._pagination import auto_paginate_items
            return auto_paginate_items(
                self.get_paginated,
                max_pages=max_pages,
                cursor_end=cursor_end,
                **{k: v for k, v in locals().items() if k not in ("self", "auto_paginate", "auto_items", "max_pages", "cursor_end", "kwargs")}
            )
        if auto_paginate:
            return auto_paginate_pages(
                self.get_paginated,
                max_pages=max_pages,
                cursor_end=cursor_end,
                limit=limit,
                country_id=country_id,
                event_types=event_types,
            )

        raw = await self._get(
            "event.getEventsPaginated",
            limit=limit,
            cursor=cursor,
            countryId=country_id,
            eventTypes=event_types,
        )
        return CursorPage.from_raw(raw, Event)


    async def paginate(self, **kwargs: typing.Any) -> typing.AsyncIterator[Event]:
        """Yield individual items across all pages seamlessly."""
        from .._pagination import paginate_items
        # Attempt to use the class default paginated method name
        fetch_fn = getattr(self, "get_paginated", None) or getattr(self, "get_many", None) or getattr(self, "get_all", None)
        if fetch_fn is None:
            raise NotImplementedError("Pagination not supported on this resource")
            
        async for item in paginate_items(fetch_fn, **kwargs):
            yield item

    async def collect_all(self, **kwargs: typing.Any) -> list[Event]:
        """Fetch all items across all pages concurrently using parallel time-slicing."""
        import warnings
        warnings.warn("`collect_all()` is deprecated. Use `get_all()` directly.", DeprecationWarning, stacklevel=2)
        import warnings
        warnings.warn("`collect_all()` is deprecated. Use `get_all()` directly.", DeprecationWarning, stacklevel=2)
        from .._pagination import parallel_collect_all
        fetch_fn = getattr(self, "get_paginated", None) or getattr(self, "get_many", None) or getattr(self, "get_all", None)
        if fetch_fn is None:
            raise NotImplementedError("Pagination not supported on this resource")
            
        return await parallel_collect_all(
            fetch_fn,
            oldest_date=kwargs.pop("oldest_date", None),
            time_slice_days=kwargs.pop("time_slice_days", 30),
            concurrency=kwargs.pop("concurrency", 500),
            **kwargs,
        )
