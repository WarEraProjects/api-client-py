from __future__ import annotations

from ..models.round_ import Hit, Round
from ._base import BaseResource


class RoundResource(BaseResource):
    """
    Endpoints:
      • round.getById
      • round.getLastHits
    """

    async def get(self, round_id: str) -> Round:
        """Get a battle round by ID."""
        raw = await self._get("round.getById", roundId=round_id)
        return Round.model_validate(raw)

    async def get_last_hits(self, round_id: str) -> list[Hit]:
        """Get the most recent hits in a battle round."""
        raw = await self._get("round.getLastHits", roundId=round_id)
        if isinstance(raw, list):
            return [Hit.model_validate(h) for h in raw]
        if isinstance(raw, dict):
            raw_items = raw.get("items", raw.get("data", []))
            items = raw_items if isinstance(raw_items, list) else []
        else:
            items = []
        return [Hit.model_validate(h) for h in items]

    async def get_many(self, round_ids: list[str]) -> list[Round | None]:
        """Fetch multiple rounds by ID concurrently using the auto-batcher."""
        import asyncio

        futs = [self.get(rid) for rid in round_ids]
        results = await asyncio.gather(*futs, return_exceptions=True)
        return [r if not isinstance(r, BaseException) else None for r in results]
