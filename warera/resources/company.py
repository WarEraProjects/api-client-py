from __future__ import annotations

import typing
from collections.abc import AsyncIterator
from datetime import datetime
from typing import Any

from ..models.common import CursorPage, ReprMixin
from ..models.company import Company
from ._base import BaseResource


class CompanyProductionBonus(ReprMixin):
    """Production bonus breakdown for a company."""

    __slots__ = (
        "strategic_bonus",
        "deposit_bonus",
        "ethic_specialization_bonus",
        "ethic_deposit_bonus",
        "total",
    )

    def __init__(
        self,
        strategic_bonus: float,
        deposit_bonus: float,
        ethic_specialization_bonus: float,
        ethic_deposit_bonus: float,
        total: float,
    ) -> None:
        self.strategic_bonus = strategic_bonus
        self.deposit_bonus = deposit_bonus
        self.ethic_specialization_bonus = ethic_specialization_bonus
        self.ethic_deposit_bonus = ethic_deposit_bonus
        self.total = total

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> CompanyProductionBonus:
        return cls(
            strategic_bonus=float(raw.get("strategicBonus", 0)),
            deposit_bonus=float(raw.get("depositBonus", 0)),
            ethic_specialization_bonus=float(raw.get("ethicSpecializationBonus", 0)),
            ethic_deposit_bonus=float(raw.get("ethicDepositBonus", 0)),
            total=float(raw.get("total", 0)),
        )


class RecommendedRegion(ReprMixin):
    """A recommended region for production of a given item."""

    __slots__ = (
        "region_id",
        "bonus",
        "deposit_bonus",
        "ethic_deposit_bonus",
        "strategic_bonus",
        "ethic_specialization_bonus",
        "tax_percent",
        "deposit_end_at",
        "item_code",
    )

    def __init__(self, raw: dict[str, Any]) -> None:
        self.region_id: str = raw.get("regionId", "")
        self.bonus: float = float(raw.get("bonus", 0))
        self.deposit_bonus: float = float(raw.get("depositBonus", 0))
        self.ethic_deposit_bonus: float = float(raw.get("ethicDepositBonus", 0))
        self.strategic_bonus: float = float(raw.get("strategicBonus", 0))
        self.ethic_specialization_bonus: float = float(raw.get("ethicSpecializationBonus", 0))
        self.tax_percent: float = float(raw.get("taxPercent", 0))
        self.deposit_end_at: str | None = raw.get("depositEndAt")
        self.item_code: str | None = raw.get("itemCode")


def _company_id_page(raw: Any) -> CursorPage[str]:
    """
    Parse ``company.getCompanies`` responses into a page of company ID strings.

    The API returns ``{items: [<id>, ...], nextCursor}`` (IDs, not full objects).
    Dict items are accepted defensively by reading ``_id`` / ``id``.
    """
    if isinstance(raw, list):
        raw_items: list[Any] = raw
        next_cursor = None
        has_more = False
    elif isinstance(raw, dict):
        candidate = raw.get("items", raw.get("data", []))
        raw_items = candidate if isinstance(candidate, list) else []
        next_cursor = raw.get("nextCursor") or raw.get("next_cursor")
        has_more = bool(raw.get("hasMore", raw.get("has_more", bool(next_cursor))))
    else:
        return CursorPage(items=[], next_cursor=None, has_more=False)

    items: list[str] = []
    for item in raw_items:
        if isinstance(item, str):
            if item:
                items.append(item)
        elif isinstance(item, dict):
            cid = item.get("_id") or item.get("id")
            if cid is not None and str(cid):
                items.append(str(cid))
        elif item is not None and str(item):
            items.append(str(item))

    return CursorPage(items=items, next_cursor=next_cursor, has_more=has_more)


class CompanyResource(BaseResource):
    """
    Endpoints:
      • company.getById
      • company.getCompanies                      (cursor-paginated, filter by userId)
      • company.getRecommendedRegionIdsByItemCode
      • company.getProductionBonus
    """

    async def get(self, company_id: str) -> Company:
        """Get a single company by ID."""
        raw = await self._get("company.getById", companyId=company_id)
        return Company.model_validate(raw)

    @typing.overload
    async def get_companies(
        self,
        *,
        user_id: str | None = None,
        per_page: int = 10,
        cursor: str | None = None,
        auto_items: typing.Literal[True],
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[str]: ...

    @typing.overload
    async def get_companies(
        self,
        *,
        user_id: str | None = None,
        per_page: int = 10,
        cursor: str | None = None,
        auto_items: typing.Literal[False] = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[str]: ...

    async def get_companies(
        self,
        *,
        user_id: str | None = None,
        per_page: int = 10,
        cursor: str | None = None,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[str] | AsyncIterator[str]:
        """
        List company IDs, optionally filtered by owner user ID (cursor-paginated).

        The WarEra API returns ID strings only. Use :meth:`get_by_user` or
        :meth:`get_many` when you need full :class:`Company` objects.
        """
        if auto_items:
            from .._pagination import auto_paginate_items

            return auto_paginate_items(
                self.get_companies,
                max_pages=max_pages,
                cursor=cursor,
                cursor_end=cursor_end,
                user_id=user_id,
                per_page=per_page,
            )

        raw = await self._get(
            "company.getCompanies",
            userId=user_id,
            perPage=per_page,
            cursor=cursor,
        )
        return _company_id_page(raw)

    async def get_by_user(self, user_id: str, **kwargs: Any) -> list[Company]:
        """
        Convenience: fetch all companies owned by a user (collects all pages).

        Paginated ID listing is hydrated via :meth:`get_many` into full
        :class:`Company` objects.
        """
        ids: list[str] = []
        async for company_id in await self.get_companies(
            user_id=user_id, auto_items=True, **kwargs
        ):
            ids.append(company_id)
        companies = await self.get_many(ids)
        return [c for c in companies if c is not None]

    async def collect_all(
        self,
        oldest_date: datetime | str | None = None,
        time_slice_days: int = 30,
        concurrency: int = 500,
        **kwargs: Any,
    ) -> list[str]:
        """
        Convenience: fetch all company IDs globally (or by country if passed)
        using parallel slicing. This is much faster than fetching sequentially.

        Returns ID strings as exposed by ``company.getCompanies``. Hydrate with
        :meth:`get_many` when full objects are needed.
        """
        from .._pagination import parallel_collect_all

        return await parallel_collect_all(
            self.get_companies,
            oldest_date=oldest_date,
            time_slice_days=time_slice_days,
            concurrency=concurrency,
            per_page=50,
            **kwargs,
        )

    async def get_recommended_regions(
        self,
        item_code: str,
        *,
        include_deposit: bool = True,
    ) -> list[RecommendedRegion]:
        """
        Get recommended regions for producing a given item, ranked by total bonus.

        Args:
            item_code:       Item code to check (e.g. ``"iron"``, ``"weapon_q1"``).
            include_deposit: Whether to include deposit bonuses in the ranking.

        Returns:
            A list of :class:`RecommendedRegion` objects sorted by bonus (best first).
        """
        raw = await self._get(
            "company.getRecommendedRegionIdsByItemCode",
            itemCode=item_code,
            includeDeposit=include_deposit,
        )
        if isinstance(raw, list):
            return [RecommendedRegion(r) for r in raw]
        if isinstance(raw, dict):
            items = raw.get("items", raw.get("data", []))
            return [RecommendedRegion(r) for r in (items if isinstance(items, list) else [])]
        return []

    async def get_production_bonus(self, company_id: str) -> CompanyProductionBonus:
        """
        Get the full production bonus breakdown for a company.

        Returns a :class:`CompanyProductionBonus` with ``strategic_bonus``,
        ``deposit_bonus``, ``ethic_specialization_bonus``, ``ethic_deposit_bonus``,
        and ``total``.
        """
        raw = await self._get("company.getProductionBonus", companyId=company_id)
        if isinstance(raw, dict):
            return CompanyProductionBonus.from_raw(raw)
        return CompanyProductionBonus.from_raw({})

    # ------------------------------------------------------------------
    # Batch helpers
    # ------------------------------------------------------------------

    async def get_many(
        self, company_ids: list[str], *, concurrency: int = 500
    ) -> list[Company | None]:
        """Fetch multiple companies by ID concurrently using the auto-batcher."""
        from .._batch import BatchSession

        if not company_ids:
            return []

        all_companies: list[Company | None] = []
        batch = BatchSession(self._http, concurrency=concurrency)
        items = []
        for cid in company_ids:
            items.append(batch.add("company.getById", {"companyId": cid}))

        await batch.flush()

        for item in items:
            if item.ok and item.result:
                all_companies.append(Company.model_validate(item.result))
            else:
                all_companies.append(None)

        return all_companies

    async def collect_by_users(
        self,
        user_ids: list[str],
        *,
        concurrency: int = 500,
    ) -> list[Company]:
        """
        Fetch all companies owned by a list of users.
        Uses native tRPC batching to group up to 50 user queries per HTTP request,
        making it extremely fast and rate-limit friendly.

        Args:
            user_ids:    List of user ID strings to fetch companies for.
            concurrency: Max concurrent requests.

        Returns:
            A flat list of all :class:`Company` objects across every user.
        """
        from .._batch import BatchSession

        if not user_ids:
            return []

        all_ids: list[str] = []
        current_queries = [{"userId": uid} for uid in user_ids]

        # Loop until all pages for all users have been fetched
        while current_queries:
            next_queries = []
            batch = BatchSession(self._http, concurrency=concurrency)

            # Queue up all current queries
            items = []
            for q in current_queries:
                items.append((q, batch.add("company.getCompanies", {**q, "perPage": 50})))

            # Flush sends them to the API in concurrent chunks of 50
            await batch.flush()

            # Process results and check for next pages
            for q, item in items:
                if item.ok:
                    page = _company_id_page(item.result)
                    all_ids.extend(page.items)
                    if page.has_more and page.next_cursor:
                        next_queries.append({**q, "cursor": page.next_cursor})

            current_queries = next_queries

        companies = await self.get_many(all_ids, concurrency=concurrency)
        return [c for c in companies if c is not None]

    async def get_recommended_region_ids_by_item_code(self, item_code: str) -> list[str]:
        """Get recommended region IDs by item code."""
        import typing

        res = await self._http.get(
            "company.getRecommendedRegionIdsByItemCode", {"itemCode": item_code}
        )
        return typing.cast(list[str], res)
