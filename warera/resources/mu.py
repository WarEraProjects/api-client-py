from __future__ import annotations

import typing
from collections.abc import AsyncIterator

from ..models.common import CursorPage
from ..models.military_unit import MilitaryUnit
from ._base import BaseResource


class MUResource(BaseResource):
    """
    Endpoints:
      • mu.getById
      • mu.getManyPaginated  (cursor-paginated)
    """

    async def get(self, mu_id: str) -> MilitaryUnit:
        """Get a military unit by ID."""
        raw = await self._get("mu.getById", muId=mu_id)
        return MilitaryUnit.model_validate(raw)

    @typing.overload
    async def get_paginated(
        self,
        *,
        limit: int = 20,
        cursor: str | None = None,
        member_id: str | None = None,
        user_id: str | None = None,
        search: str | None = None,
        auto_items: typing.Literal[True],
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[MilitaryUnit]: ...

    @typing.overload
    async def get_paginated(
        self,
        *,
        limit: int = 20,
        cursor: str | None = None,
        member_id: str | None = None,
        user_id: str | None = None,
        search: str | None = None,
        auto_items: typing.Literal[False] = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[MilitaryUnit]: ...

    async def get_paginated(
        self,
        *,
        limit: int = 20,
        cursor: str | None = None,
        member_id: str | None = None,
        user_id: str | None = None,
        search: str | None = None,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[MilitaryUnit] | AsyncIterator[MilitaryUnit]:
        """
        Get military units (cursor-paginated).

        Args:
            member_id:  Filter: MUs that this user is a member of.
            user_id:    Filter: MUs owned/created by this user.
            search:     Text search across MU names.
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
            "mu.getManyPaginated",
            limit=limit,
            cursor=cursor,
            memberId=member_id,
            userId=user_id,
            search=search,
        )
        return CursorPage.from_raw(raw, MilitaryUnit)

    async def get_many(self, mu_ids: list[str]) -> list[MilitaryUnit | None]:
        """Fetch multiple military units by ID concurrently using the auto-batcher."""
        import asyncio

        futs = [self.get(mid) for mid in mu_ids]
        results = await asyncio.gather(*futs, return_exceptions=True)
        return [r if not isinstance(r, BaseException) else None for r in results]

    async def collect_all(self, **kwargs: typing.Any) -> list[MilitaryUnit]:
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
