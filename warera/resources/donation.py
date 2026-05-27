from __future__ import annotations

import typing
from collections.abc import AsyncIterator

from .._pagination import auto_paginate_pages
from ..models.common import CursorPage
from ..models.donation import Donation, DonationTotals
from ._base import BaseResource


class DonationResource(BaseResource):
    """
    Endpoints:
      • donation.getManyPaginated  (cursor-paginated)
      • donation.getTotalDonations
    """

    @typing.overload
    async def get_paginated(
        self,
        *,
        mu_id: str | None = None,
        country_id: str | None = None,
        party_id: str | None = None,
        limit: int = 20,
        cursor: str | None = None,
        direction: str | None = None,
        auto_paginate: typing.Literal[False] = False,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Donation]: ...

    @typing.overload
    async def get_paginated(
        self,
        *,
        mu_id: str | None = None,
        country_id: str | None = None,
        party_id: str | None = None,
        limit: int = 20,
        cursor: str | None = None,
        direction: str | None = None,
        auto_paginate: typing.Literal[True],
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[CursorPage[Donation]]: ...

    async def get_paginated(
        self,
        *,
        mu_id: str | None = None,
        country_id: str | None = None,
        party_id: str | None = None,
        limit: int = 20,
        cursor: str | None = None,
        direction: str | None = None,
        auto_paginate: bool = False,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Donation] | AsyncIterator[CursorPage[Donation]] | AsyncIterator[Donation]:
        """
        Get donations (cursor-paginated), filtered by target entity.

        At least one of ``mu_id``, ``country_id``, or ``party_id`` is recommended.

        Args:
            direction: ``"forward"`` (default) or ``"backward"`` pagination.
        """
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
                mu_id=mu_id,
                country_id=country_id,
                party_id=party_id,
                limit=limit,
                direction=direction,
            )

        raw = await self._get(
            "donation.getManyPaginated",
            muId=mu_id,
            countryId=country_id,
            partyId=party_id,
            limit=limit,
            cursor=cursor,
            direction=direction,
        )
        return CursorPage.from_raw(raw, Donation)

    async def get_totals(
        self,
        *,
        mu_id: str | None = None,
        country_id: str | None = None,
        party_id: str | None = None,
    ) -> DonationTotals:
        """
        Get aggregate donation totals (total amount and donor count) for a target.

        Args:
            mu_id:      Military unit to aggregate for.
            country_id: Country to aggregate for.
            party_id:   Party to aggregate for.
        """
        raw = await self._get(
            "donation.getTotalDonations",
            muId=mu_id,
            countryId=country_id,
            partyId=party_id,
        )
        return DonationTotals.model_validate(raw)


    async def paginate(self, **kwargs: typing.Any) -> typing.AsyncIterator[Donation]:
        """Yield individual items across all pages seamlessly."""
        from .._pagination import paginate_items
        # Attempt to use the class default paginated method name
        fetch_fn = getattr(self, "get_paginated", None) or getattr(self, "get_many", None) or getattr(self, "get_all", None)
        if fetch_fn is None:
            raise NotImplementedError("Pagination not supported on this resource")
            
        async for item in paginate_items(fetch_fn, **kwargs):
            yield item

    async def collect_all(self, **kwargs: typing.Any) -> list[Donation]:
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
            time_slice_days=kwargs.pop("time_slice_days", 0.2),
            concurrency=kwargs.pop("concurrency", 500),
            **kwargs,
        )
