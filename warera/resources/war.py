"""War resource — wraps war.getById."""

from __future__ import annotations

from ..models.war import War
from ._base import BaseResource


class WarResource(BaseResource):
    """
    Endpoints:
      • war.getById
    """

    async def get(self, war_id: str) -> War:
        """Get a war by its ID."""
        raw = await self._get("war.getById", warId=war_id)
        return War.model_validate(raw)
