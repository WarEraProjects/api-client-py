from __future__ import annotations

import typing
from collections.abc import AsyncIterator
from typing import Any

from .._enums import BattleDirection, BattleFilter
from ..models.battle import Battle, BattleLive
from ..models.common import CursorPage
from ._base import BaseResource


class BattleResource(BaseResource):
    """
    Endpoints:
      • battle.getById
      • battle.getLiveBattleData
      • battle.getBattles  (cursor-paginated)
    """

    async def get(self, battle_id: str) -> Battle:
        """Get full battle info by ID."""
        raw = await self._get("battle.getById", battleId=battle_id)
        return Battle.model_validate(raw)

    async def get_live(
        self,
        battle_id: str,
        *,
        round_number: int | None = None,
    ) -> BattleLive:
        """Get live battle data (scores, damage, time remaining)."""
        raw = await self._get(
            "battle.getLiveBattleData",
            battleId=battle_id,
            roundNumber=round_number,
        )
        return BattleLive.model_validate(raw)

    @typing.overload
    async def get_many(
        self,
        *,
        is_active: bool | None = None,
        limit: int = 10,
        cursor: str | None = None,
        direction: BattleDirection | str | None = None,
        filter: BattleFilter | str | None = None,
        defender_region_id: str | None = None,
        war_id: str | None = None,
        country_id: str | None = None,
        auto_items: typing.Literal[True],
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[Battle]: ...

    @typing.overload
    async def get_many(
        self,
        *,
        is_active: bool | None = None,
        limit: int = 10,
        cursor: str | None = None,
        direction: BattleDirection | str | None = None,
        filter: BattleFilter | str | None = None,
        defender_region_id: str | None = None,
        war_id: str | None = None,
        country_id: str | None = None,
        auto_items: typing.Literal[False] = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Battle]: ...

    async def get_many(
        self,
        *,
        is_active: bool | None = None,
        limit: int = 10,
        cursor: str | None = None,
        direction: BattleDirection | str | None = None,
        filter: BattleFilter | str | None = None,
        defender_region_id: str | None = None,
        war_id: str | None = None,
        country_id: str | None = None,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Battle] | AsyncIterator[Battle]:
        """Get battles with optional filters (cursor-paginated)."""
        if auto_items:
            from .._pagination import auto_paginate_items

            return auto_paginate_items(
                self.get_many,
                max_pages=max_pages,
                cursor=cursor,
                cursor_end=cursor_end,
                is_active=is_active,
                limit=limit,
                direction=direction,
                filter=filter,
                defender_region_id=defender_region_id,
                war_id=war_id,
                country_id=country_id,
            )

        raw = await self._get(
            "battle.getBattles",
            isActive=is_active,
            limit=limit,
            cursor=cursor,
            direction=direction,
            filter=filter,
            defenderRegionId=defender_region_id,
            warId=war_id,
            countryId=country_id,
        )
        return CursorPage.from_raw(raw, Battle)

    async def get_active(self, **kwargs: Any) -> list[Battle]:
        """Convenience: fetch all active battles across the globe."""
        items = []
        async for item in await self.get_many(is_active=True, auto_items=True, **kwargs):
            items.append(item)
        return items


    async def collect_all(self, **kwargs: typing.Any) -> list[Battle]:
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
