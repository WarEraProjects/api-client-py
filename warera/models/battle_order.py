from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import WareraModel


class BattleOrder(WareraModel):
    """A battle order placed by a military unit for a specific battle and side."""

    battle_id: str | None = Field(default=None, description="The battle id.")
    side: str | None = Field(default=None, description="The side.")
    mu_id: str | None = Field(default=None, description="The mu id.")
    mu_name: str | None = Field(default=None, description="The mu name.")
    country_id: str | None = Field(default=None, description="The country id.")
    details: dict[str, Any] | None = Field(default=None, description="The details.")
