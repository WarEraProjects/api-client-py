from __future__ import annotations

import typing
from collections.abc import AsyncIterator
from typing import Any

from .._enums import ActionLogActionType
from ..models.action_log import ActionLog
from ..models.common import CursorPage
from ._base import BaseResource


class ActionLogResource(BaseResource):
    """
    Endpoints:
      • actionLog.getPaginated  (cursor-paginated)
    """

    @typing.overload
    async def get_many(
        self,
        *,
        limit: int = 20,
        cursor: str | None = None,
        user_id: str | None = None,
        mu_id: str | None = None,
        country_id: str | None = None,
        action_type: ActionLogActionType | str | None = None,
        auto_items: typing.Literal[True],
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[ActionLog]: ...

    @typing.overload
    async def get_many(
        self,
        *,
        limit: int = 20,
        cursor: str | None = None,
        user_id: str | None = None,
        mu_id: str | None = None,
        country_id: str | None = None,
        action_type: ActionLogActionType | str | None = None,
        auto_items: typing.Literal[False] = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[ActionLog]: ...

    async def get_many(
        self,
        *,
        limit: int = 20,
        cursor: str | None = None,
        user_id: str | None = None,
        mu_id: str | None = None,
        country_id: str | None = None,
        action_type: ActionLogActionType | str | None = None,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[ActionLog] | AsyncIterator[ActionLog]:
        """
        Get paginated action logs with optional filtering.

        Args:
            limit:       Number of results per page (1-100, default 20).
            cursor:      Pagination cursor for the next page.
            user_id:     Filter by user ID.
            mu_id:       Filter by military unit ID.
            country_id:  Filter by country ID.
            action_type: Filter by action type.
        """
        if auto_items:
            from .._pagination import auto_paginate_items

            return auto_paginate_items(
                self.get_many,
                max_pages=max_pages,
                cursor_end=cursor_end,
                limit=limit,
                user_id=user_id,
                mu_id=mu_id,
                country_id=country_id,
                action_type=action_type,
            )

        raw = await self._get(
            "actionLog.getPaginated",
            limit=limit,
            cursor=cursor,
            userId=user_id,
            muId=mu_id,
            countryId=country_id,
            actionType=action_type,
        )
        return CursorPage.from_raw(raw, ActionLog)

    async def get_all(self, **kwargs: Any) -> list[ActionLog]:
        """Convenience: collect all action logs matching the given filters."""
        items = []
        async for item in await self.get_many(auto_items=True, **kwargs):
            items.append(item)
        return items


    async def collect_all(self, **kwargs: typing.Any) -> list[ActionLog]:
        """Fetch all items across all pages concurrently using parallel time-slicing."""
        import warnings

        warnings.warn(
            "`collect_all()` is deprecated. Use `get_all()` directly.",
            DeprecationWarning,
            stacklevel=2,
        )
        from .._pagination import parallel_collect_all

        fetch_fn = (
            getattr(self, "get_paginated", None)
            or getattr(self, "get_many", None)
            or getattr(self, "get_all", None)
        )
        if fetch_fn is None:
            raise NotImplementedError("Pagination not supported on this resource")

        return await parallel_collect_all(
            fetch_fn,
            oldest_date=kwargs.pop("oldest_date", None),
            time_slice_days=kwargs.pop("time_slice_days", 0.2),
            concurrency=kwargs.pop("concurrency", 500),
            **kwargs,
        )
