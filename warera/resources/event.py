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
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Event] | AsyncIterator[CursorPage[Event]]:
        """Get game events, optionally filtered by country and/or event type."""
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
