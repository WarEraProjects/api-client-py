from __future__ import annotations

import asyncio
import contextlib
import typing
from collections.abc import AsyncIterator
from datetime import datetime
from typing import Any

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
        auto_items: typing.Literal[True],
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[UserLite]: ...

    @typing.overload
    async def get_by_country(
        self,
        country_id: str,
        *,
        limit: int = 10,
        cursor: str | None = None,
        auto_items: typing.Literal[False] = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[UserLite]: ...

    async def get_by_country(
        self,
        country_id: str,
        *,
        limit: int = 10,
        cursor: str | None = None,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[UserLite] | AsyncIterator[UserLite]:
        """Get users belonging to a country (cursor-paginated)."""
        if auto_items:
            from .._pagination import auto_paginate_items

            return auto_paginate_items(
                self.get_by_country,
                max_pages=max_pages,
                cursor=cursor,
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

    async def collect_by_country(
        self,
        country_id: str,
        oldest_date: datetime | str | None = None,
        time_slice_days: int = 30,
        concurrency: int = 500,
        **kwargs: Any,
    ) -> list[UserLite]:
        """Return all users in a country as a flat list, fetched in parallel."""
        from .._pagination import parallel_collect_all

        return await parallel_collect_all(
            self.get_by_country,
            oldest_date=oldest_date,
            time_slice_days=time_slice_days,
            concurrency=concurrency,
            country_id=country_id,
            **kwargs,
        )

    async def collect_all(self, *, concurrency: int = 500) -> list[UserLite]:
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
                # We use collect_by_country, but set its concurrency low to not exhaust the semaphore
                # since we're already scaling concurrency horizontally across countries.
                return await self.collect_by_country(country_id=cid, limit=100, concurrency=500)

        results = await asyncio.gather(*[fetch_for_country(cid) for cid in country_ids])

        all_users = [user for users in results for user in users]
        # Attempt to sort globally
        with contextlib.suppress(Exception):
            all_users.sort(
                key=lambda x: getattr(x, "created_at", getattr(x, "createdAt", "")), reverse=True
            )

        return all_users

    # ------------------------------------------------------------------
    # Batch helper
    # ------------------------------------------------------------------

    async def get_many(self, user_ids: list[str], *, concurrency: int = 500) -> list[User | None]:
        """Fetch multiple users by ID concurrently using the auto-batcher."""
        from .._batch import BatchSession

        if not user_ids:
            return []

        all_users: list[User | None] = []
        batch = BatchSession(self._http, concurrency=concurrency)
        items = []
        for uid in user_ids:
            items.append(batch.add("user.getUserById", {"userId": uid}))

        await batch.flush()

        for item in items:
            if item.ok and item.result:
                all_users.append(User.model_validate(item.result))
            else:
                all_users.append(None)

        return all_users
