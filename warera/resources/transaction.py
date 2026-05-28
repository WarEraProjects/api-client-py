from __future__ import annotations

import typing
from collections.abc import AsyncIterator
from datetime import datetime

from .._enums import TransactionType
from ..models.common import CursorPage
from ..models.transaction import Transaction
from ._base import BaseResource


class TransactionResource(BaseResource):
    """
    Endpoints:
      • transaction.getPaginatedTransactions  (cursor-paginated)
    """

    @typing.overload
    async def get_paginated(
        self,
        *,
        limit: int = 10,
        cursor: str | None = None,
        user_id: str | None = None,
        mu_id: str | None = None,
        country_id: str | None = None,
        party_id: str | None = None,
        item_code: str | None = None,
        transaction_type: TransactionType | str | list[TransactionType | str] | None = None,
        auto_items: typing.Literal[True],
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[Transaction]: ...

    @typing.overload
    async def get_paginated(
        self,
        *,
        limit: int = 10,
        cursor: str | None = None,
        user_id: str | None = None,
        mu_id: str | None = None,
        country_id: str | None = None,
        party_id: str | None = None,
        item_code: str | None = None,
        transaction_type: TransactionType | str | list[TransactionType | str] | None = None,
        auto_items: typing.Literal[False] = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Transaction]: ...

    async def get_paginated(
        self,
        *,
        limit: int = 10,
        cursor: str | None = None,
        user_id: str | None = None,
        mu_id: str | None = None,
        country_id: str | None = None,
        party_id: str | None = None,
        item_code: str | None = None,
        transaction_type: TransactionType | str | list[TransactionType | str] | None = None,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Transaction] | AsyncIterator[Transaction]:
        """
        Get paginated transactions with optional filters.

        `transaction_type` uniquely accepts a single type string OR a list — both are
        valid per the API schema. When a list is passed it is serialised as-is.
        """
        if auto_items:
            from .._pagination import auto_paginate_items

            return auto_paginate_items(
                self.get_paginated,
                max_pages=max_pages,
                cursor=cursor,
                cursor_end=cursor_end,
                limit=limit,
                user_id=user_id,
                mu_id=mu_id,
                country_id=country_id,
                party_id=party_id,
                item_code=item_code,
                transaction_type=transaction_type,
            )

        raw = await self._get(
            "transaction.getPaginatedTransactions",
            limit=limit,
            cursor=cursor,
            userId=user_id,
            muId=mu_id,
            countryId=country_id,
            partyId=party_id,
            itemCode=item_code,
            transactionType=transaction_type,
        )
        return CursorPage.from_raw(raw, Transaction)

    async def collect_all(
        self,
        *,
        oldest_date: datetime | str,
        limit: int = 100,
        user_id: str | None = None,
        mu_id: str | None = None,
        country_id: str | None = None,
        party_id: str | None = None,
        item_code: str | None = None,
        transaction_type: TransactionType | str | list[TransactionType | str] | None = None,
        time_slice_days: float = 0.2,
        concurrency: int = 500,
    ) -> list[Transaction]:
        """
        Fetch all transactions back to `oldest_date` using parallel time-slicing.
        By forging synthetic cursors for intermediate dates, this method bypasses the
        sequential dependency of cursor pagination and allows fetching chunks concurrently.
        Because the chunks are fetched concurrently, the underlying HTTP client will
        automatically batch them into single POST requests.
        """
        from .._pagination import parallel_collect_all

        return await parallel_collect_all(
            self.get_paginated,
            oldest_date=oldest_date,
            time_slice_days=time_slice_days,
            concurrency=concurrency,
            limit=limit,
            user_id=user_id,
            mu_id=mu_id,
            country_id=country_id,
            party_id=party_id,
            item_code=item_code,
            transaction_type=transaction_type,
        )
