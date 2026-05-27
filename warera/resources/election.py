from __future__ import annotations

import typing
from collections.abc import AsyncIterator

from .._pagination import auto_paginate_pages
from ..models.common import CursorPage
from ..models.election import Election
from ._base import BaseResource


class ElectionResource(BaseResource):
    """
    Endpoints:
      • election.getElections  (cursor-paginated)
    """

    @typing.overload
    async def get_paginated(
        self,
        *,
        country_id: str | None = None,
        limit: int = 20,
        cursor: str | None = None,
        direction: str | None = None,
        auto_paginate: typing.Literal[False] = False,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Election]: ...

    @typing.overload
    async def get_paginated(
        self,
        *,
        country_id: str | None = None,
        limit: int = 20,
        cursor: str | None = None,
        direction: str | None = None,
        auto_paginate: typing.Literal[True],
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[CursorPage[Election]]: ...

    async def get_paginated(
        self,
        *,
        country_id: str | None = None,
        limit: int = 20,
        cursor: str | None = None,
        direction: str | None = None,
        auto_paginate: bool = False,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Election] | AsyncIterator[CursorPage[Election]] | AsyncIterator[Election]:
        """
        Get elections (cursor-paginated), optionally filtered by country.

        Args:
            country_id: Filter to elections in this country.
            direction:  ``"forward"`` (default) or ``"backward"`` pagination.
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
                country_id=country_id,
                limit=limit,
                direction=direction,
            )

        raw = await self._get(
            "election.getElections",
            countryId=country_id,
            limit=limit,
            cursor=cursor,
            direction=direction,
        )
        return CursorPage.from_raw(raw, Election)

    async def get_by_country(self, country_id: str) -> list[Election]:
        """Convenience: fetch all elections in a given country."""
        items = []
        async for page in await self.get_paginated(country_id=country_id, auto_paginate=True):
            items.extend(page.items)
        return items


    async def paginate(self, **kwargs: typing.Any) -> typing.AsyncIterator[Election]:
        """Yield individual items across all pages seamlessly."""
        from .._pagination import paginate_items
        # Attempt to use the class default paginated method name
        fetch_fn = getattr(self, "get_paginated", None) or getattr(self, "get_many", None) or getattr(self, "get_all", None)
        if fetch_fn is None:
            raise NotImplementedError("Pagination not supported on this resource")
            
        async for item in paginate_items(fetch_fn, **kwargs):
            yield item

    async def collect_all(self, **kwargs: typing.Any) -> list[Election]:
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
