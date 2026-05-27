from __future__ import annotations

import asyncio
import typing
from collections.abc import AsyncIterator
from typing import Any

from .._pagination import auto_paginate_pages
from ..models.common import CursorPage
from ..models.user import User, UserLite
from ._base import BaseResource


class UserResource(BaseResource):
    """
    Endpoints:
      • user.getUserById
      • user.getUserLite
      • user.getUsersByCountry  (cursor-paginated)
    """

    async def get_by_id(self, user_id: str) -> User:
        """Get a user's profile by ID."""
        raw = await self._get("user.getUserById", userId=user_id)
        return User.model_validate(raw)

    async def get_lite(self, user_id: str) -> UserLite:
        """Get a user's lite profile by ID. (Deprecated in favor of get_by_id)"""
        raw = await self._get("user.getUserLite", userId=user_id)
        return UserLite.model_validate(raw)

    @typing.overload
    async def get_by_country(
        self,
        country_id: str,
        *,
        limit: int = 10,
        cursor: str | None = None,
        auto_paginate: typing.Literal[False] = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[UserLite]: ...

    @typing.overload
    async def get_by_country(
        self,
        country_id: str,
        *,
        limit: int = 10,
        cursor: str | None = None,
        auto_paginate: typing.Literal[True],
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[CursorPage[UserLite]]: ...

    async def get_by_country(
        self,
        country_id: str,
        *,
        limit: int = 10,
        cursor: str | None = None,
        auto_paginate: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[UserLite] | AsyncIterator[CursorPage[UserLite]]:
        """Get users belonging to a country (cursor-paginated)."""
        if auto_paginate:
            return auto_paginate_pages(
                self.get_by_country,
                max_pages=max_pages,
                cursor_end=cursor_end,
                country_id=country_id,
                limit=limit,
            )

        raw = await self._get(
            "user.getUsersByCountry",
            countryId=country_id,
            limit=limit,
            cursor=cursor,
        )
        return CursorPage.from_raw(raw, UserLite)

    async def collect_by_country(self, country_id: str, **kwargs: Any) -> list[UserLite]:
        """Return all users in a country as a flat list."""
        items = []
        async for page in await self.get_by_country(country_id=country_id, auto_paginate=True, **kwargs):
            items.extend(page.items)
        return items

    async def collect_all(self, *, concurrency: int = 20) -> list[UserLite]:
        """
        Fetch every user from every country concurrently using auto pagination.

        This is the fastest way to retrieve all users in the game. It:
          1. Fetches all country IDs via ``country.getAllCountries``.
          2. Concurrently paginates through users for all countries.

        Args:
            concurrency: Max concurrent requests.

        Returns:
            A flat list of all :class:`UserLite` objects across every country.
        """
        from .country import CountryResource

        country_resource = CountryResource(self._http)
        countries = await country_resource.get_all()
        country_ids = list(countries.keys())

        if not country_ids:
            return []

        sem = asyncio.Semaphore(concurrency)

        async def fetch_for_country(cid: str) -> list[UserLite]:
            async with sem:
                items = []
                async for page in await self.get_by_country(country_id=cid, limit=50, auto_paginate=True):
                    items.extend(page.items)
                return items

        results = await asyncio.gather(*[fetch_for_country(cid) for cid in country_ids])
        return [user for users in results for user in users]

    # ------------------------------------------------------------------
    # Batch helper
    # ------------------------------------------------------------------

    async def get_many(self, user_ids: list[str]) -> list[User | None]:
        """Fetch multiple users by ID concurrently using the auto-batcher."""
        import asyncio

        
        futs = [self.get_by_id(uid) for uid in user_ids]
        results = await asyncio.gather(*futs, return_exceptions=True)
        return [r if not isinstance(r, BaseException) else None for r in results]
