from __future__ import annotations

import typing
from collections.abc import AsyncIterator

from ..models.alliance import Alliance
from ..models.common import CursorPage
from ._base import BaseResource


class AllianceResource(BaseResource):
    """
    Endpoints:
      • alliance.getById
      • alliance.getByIds
      • alliance.getManyPaginated  (cursor-paginated)
    """

    async def get(self, alliance_id: str) -> Alliance:
        """Get a single alliance by ID."""
        raw = await self._get("alliance.getById", allianceId=alliance_id)
        return Alliance.model_validate(raw)

    async def get_many(self, ids: list[str]) -> list[Alliance]:
        """Get multiple alliances by their IDs."""
        raw = await self._get("alliance.getByIds", ids=ids)
        if isinstance(raw, list):
            return [Alliance.model_validate(x) for x in raw]
        return []

    @typing.overload
    async def get_paginated(
        self,
        *,
        limit: int = 20,
        cursor: str | None = None,
        auto_items: typing.Literal[True],
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[Alliance]: ...

    @typing.overload
    async def get_paginated(
        self,
        *,
        limit: int = 20,
        cursor: str | None = None,
        auto_items: typing.Literal[False] = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Alliance]: ...

    async def get_paginated(
        self,
        *,
        limit: int = 20,
        cursor: str | None = None,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Alliance] | AsyncIterator[Alliance]:
        """
        Get alliances (cursor-paginated).
        """
        if auto_items:
            from .._pagination import auto_paginate_items

            return auto_paginate_items(
                self.get_paginated,
                max_pages=max_pages,
                cursor_end=cursor_end,
                **{
                    k: v
                    for k, v in locals().items()
                    if k
                    not in (
                        "self",
                        "auto_paginate",
                        "auto_items",
                        "max_pages",
                        "cursor_end",
                        "kwargs",
                    )
                },
            )

        raw = await self._get(
            "alliance.getManyPaginated",
            limit=limit,
            cursor=cursor,
        )
        return CursorPage.from_raw(raw, Alliance)


    async def collect_all(self, **kwargs: typing.Any) -> list[Alliance]:
        """Fetch all items across all pages concurrently using parallel time-slicing."""
        import warnings

        warnings.warn(
            "`collect_all()` is deprecated. Use `get_paginated(auto_items=True)` directly.",
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
