from __future__ import annotations

from .._cache import async_memoize
from ..models.region import Region
from ._base import BaseResource


class RegionResource(BaseResource):
    """
    Endpoints:
      • region.getById
      • region.getRegionsObject
    """

    async def get(self, region_id: str) -> Region:
        """Get a single region by ID."""
        raw = await self._get("region.getById", regionId=region_id)
        return Region.model_validate(raw)

    @async_memoize
    async def get_all(self) -> dict[str, Region]:
        """
        Get all regions as a dict keyed by region ID.
        """
        raw = await self._get("region.getRegionsObject")
        if isinstance(raw, dict):
            return {k: Region.model_validate(v) for k, v in raw.items()}
        if isinstance(raw, list):
            regions = [Region.model_validate(r) for r in raw]
            return {r.id: r for r in regions if r.id}
        return {}

    async def get_many(self, region_ids: list[str]) -> list[Region | None]:
        """Fetch multiple regions by ID concurrently using the auto-batcher."""
        import asyncio

        futs = [self.get(rid) for rid in region_ids]
        results = await asyncio.gather(*futs, return_exceptions=True)
        return [r if not isinstance(r, BaseException) else None for r in results]
