from __future__ import annotations

import typing
from collections.abc import AsyncIterator
from typing import Any

from ..models.common import CursorPage, ReprMixin
from ..models.work_offer import WorkOffer
from ._base import BaseResource


class WageRange(ReprMixin):
    """Min/max/average wage range."""

    __slots__ = ("min", "max", "average")

    def __init__(self, raw: dict[str, Any]) -> None:
        self.min: float = float(raw.get("min", 0))
        self.max: float = float(raw.get("max", 0))
        self.average: float = float(raw.get("average", 0))


class WageStats(ReprMixin):
    """
    Result of ``workOffer.getWageStats``.

    Attributes:
        allowed_range:        Min/max/average wages allowed for the given worker profile.
        top_offer:            Highest absolute offer on the market.
        top_eligible_offer:   Best offer this worker qualifies for.
        top_eligible_offers:  List of top raw offer dicts this worker qualifies for.
    """

    def __init__(self, raw: dict[str, Any]) -> None:
        self.allowed_range = WageRange(raw.get("allowedRange", {}))
        self.top_offer: float = float(raw.get("topOffer", 0))
        self.top_eligible_offer: float = float(raw.get("topEligibleOffer", 0))
        self.top_eligible_offers: list[dict[str, Any]] = raw.get("topEligibleOffers", [])


class WorkOfferResource(BaseResource):
    """
    Endpoints:
      • workOffer.getById
      • workOffer.getWorkOfferByCompanyId
      • workOffer.getWorkOffersPaginated   (cursor-paginated)
      • workOffer.getWageStats
    """

    async def get(self, work_offer_id: str) -> WorkOffer:
        """Get a single work offer by ID."""
        raw = await self._get("workOffer.getById", workOfferId=work_offer_id)
        return WorkOffer.model_validate(raw)

    async def get_by_company(self, company_id: str) -> list[WorkOffer]:
        """Get all work offers posted by a specific company."""
        raw = await self._get("workOffer.getWorkOfferByCompanyId", companyId=company_id)
        if isinstance(raw, list):
            return [WorkOffer.model_validate(o) for o in raw]
        if isinstance(raw, dict):
            raw_items = raw.get("items", raw.get("data", []))
            items = raw_items if isinstance(raw_items, list) else []
        else:
            items = []
        return [WorkOffer.model_validate(o) for o in items]

    @typing.overload
    async def get_paginated(
        self,
        *,
        limit: int = 10,
        cursor: str | None = None,
        user_id: str | None = None,
        region_id: str | None = None,
        energy: float | None = None,
        production: float | None = None,
        level: float | None = None,
        citizenship: str | None = None,
        auto_items: typing.Literal[True],
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[WorkOffer]: ...

    @typing.overload
    async def get_paginated(
        self,
        *,
        limit: int = 10,
        cursor: str | None = None,
        user_id: str | None = None,
        region_id: str | None = None,
        energy: float | None = None,
        production: float | None = None,
        level: float | None = None,
        citizenship: str | None = None,
        auto_items: typing.Literal[False] = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[WorkOffer]: ...

    async def get_paginated(
        self,
        *,
        limit: int = 10,
        cursor: str | None = None,
        user_id: str | None = None,
        region_id: str | None = None,
        energy: float | None = None,
        production: float | None = None,
        level: float | None = None,
        citizenship: str | None = None,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[WorkOffer] | AsyncIterator[WorkOffer]:
        """
        Get work offers with optional filters (cursor-paginated).

        Args:
            energy:      Filter: offers requiring at most this energy.
            production:  Filter: offers with at least this production value.
            level:       Filter: offers requiring at most this user level.
            citizenship: Filter: offers open to this citizenship.
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
            "workOffer.getWorkOffersPaginated",
            limit=limit,
            cursor=cursor,
            userId=user_id,
            regionId=region_id,
            energy=energy,
            production=production,
            level=level,
            citizenship=citizenship,
        )
        return CursorPage.from_raw(raw, WorkOffer)

    async def get_wage_stats(
        self,
        *,
        energy: float,
        production: float,
        citizenship: str,
    ) -> WageStats:
        """
        Get wage statistics for a given worker profile — the range of allowed wages,
        the top market offer, and the best offers this worker is eligible for.

        Args:
            energy:      The worker's energy stat.
            production:  The worker's production stat.
            citizenship: The worker's citizenship country ID or code.

        Returns:
            A :class:`WageStats` object.
        """
        raw = await self._get(
            "workOffer.getWageStats",
            energy=energy,
            production=production,
            citizenship=citizenship,
        )
        if isinstance(raw, dict):
            return WageStats(raw)
        return WageStats({})

    async def collect_all(self, **kwargs: typing.Any) -> list[WorkOffer]:
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
