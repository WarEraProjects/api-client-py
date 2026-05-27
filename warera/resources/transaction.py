from __future__ import annotations

import typing
from collections.abc import AsyncIterator

from .._enums import TransactionType
from .._pagination import auto_paginate_pages
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
        auto_paginate: typing.Literal[False] = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Transaction]: ...

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
        auto_paginate: typing.Literal[True],
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[CursorPage[Transaction]]: ...

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
        auto_paginate: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[Transaction] | AsyncIterator[CursorPage[Transaction]]:
        """
        Get paginated transactions with optional filters.

        `transaction_type` uniquely accepts a single type string OR a list — both are
        valid per the API schema. When a list is passed it is serialised as-is.
        """
        if auto_paginate:
            return auto_paginate_pages(
                self.get_paginated,
                max_pages=max_pages,
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
