from __future__ import annotations

import asyncio
import typing
from collections.abc import AsyncIterator
from datetime import datetime, timedelta, timezone

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
        time_slice_days: int = 30,
        concurrency: int = 20,
    ) -> list[Transaction]:
        """
        Fetch all transactions back to `oldest_date` using parallel time-slicing.
        By forging synthetic cursors for intermediate dates, this method bypasses the
        sequential dependency of cursor pagination and allows fetching chunks concurrently.
        Because the chunks are fetched concurrently, the underlying HTTP client will
        automatically batch them into single POST requests.
        """
        if isinstance(oldest_date, str):
            oldest_date = oldest_date.replace("Z", "+00:00")
            oldest_date = datetime.fromisoformat(oldest_date)
        if oldest_date.tzinfo is None:
            oldest_date = oldest_date.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        
        # Generate time chunks
        chunks: list[tuple[str | None, datetime]] = []
        current_end = now
        
        while current_end > oldest_date:
            chunk_start = max(oldest_date, current_end - timedelta(days=time_slice_days))
            
            # We need a cursor representing `current_end` (unless it's the very first chunk).
            # A synthetic cursor is just the ISO date string + a dummy MongoDB ID.
            if current_end == now:
                cursor = None
            else:
                # Format: 2026-03-28T05:28:52.832Z|000000000000000000000000
                iso_str = current_end.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                cursor = f"{iso_str}|000000000000000000000000"
                
            chunks.append((cursor, chunk_start))
            current_end = chunk_start
            
        all_transactions: list[Transaction] = []
        sem = asyncio.Semaphore(concurrency)
        
        async def fetch_chunk(cur: str | None, cur_end: datetime) -> list[Transaction]:
            chunk_txs: list[Transaction] = []
            async with sem:
                async for page in await self.get_paginated(
                    auto_paginate=True,
                    limit=limit,
                    cursor=cur,
                    cursor_end=cur_end.isoformat(),
                    user_id=user_id,
                    mu_id=mu_id,
                    country_id=country_id,
                    party_id=party_id,
                    item_code=item_code,
                    transaction_type=transaction_type,
                ):
                    chunk_txs.extend(page.items)
            return chunk_txs
            
        chunk_results = await asyncio.gather(*[
            fetch_chunk(c, start) for c, start in chunks
        ])
        
        for res in chunk_results:
            all_transactions.extend(res)
            
        # Sort descending by created_at since the chunks were fetched out of order,
        # and deduplicate by ID just in case there was boundary overlap.
        seen = set()
        unique_txs = []
        for tx in all_transactions:
            if tx.id not in seen:
                seen.add(tx.id)
                unique_txs.append(tx)
                
        unique_txs.sort(key=lambda x: x.created_at or "", reverse=True)
        return unique_txs
