from __future__ import annotations

from typing import TYPE_CHECKING

from ..models.country import Country
from ._base import BaseResource

if TYPE_CHECKING:
    pass


class CountryResource(BaseResource):
    """
    Endpoints:
      • country.getCountryById
      • country.getAllCountries
    """

    async def get(self, country_id: str) -> Country:
        """Get a single country by ID."""
        raw = await self._get("country.getCountryById", countryId=country_id)
        return Country.model_validate(raw)

    async def get_all(self) -> dict[str, Country]:
        """
        Get all countries.
        Returns a dict keyed by country ID for O(1) lookups.
        """
        raw = await self._get_swr("country.getAllCountries", ttl_seconds=3600)
        if isinstance(raw, dict):
            return {k: Country.model_validate(v) for k, v in raw.items()}
        if isinstance(raw, list):
            countries = [Country.model_validate(c) for c in raw]
            return {c.id: c for c in countries if c.id}
        return {}

    async def find_by_name(self, name: str) -> Country | None:
        """
        Client-side helper: return the country matching `name` (case-insensitive).

        Returns None if no country with that name exists.
        """
        countries = await self.get_all()
        name_lower = name.lower()
        for country in countries.values():
            if country.name and country.name.lower() == name_lower:
                return country
        return None
