from __future__ import annotations

from ..models.government import Government
from ._base import BaseResource


class GovernmentResource(BaseResource):
    """
    Endpoints:
      • government.getByCountryId
    """

    async def get(self, country_id: str) -> Government:
        """Get the government snapshot for a country."""
        raw = await self._get("government.getByCountryId", countryId=country_id)
        return Government.model_validate(raw)

    async def get_by_country_id(self, country_id: str) -> Government:
        """Get government by country ID."""
        res = await self._http.get("government.getByCountryId", {"countryId": country_id})
        return Government.parse_obj(res)
