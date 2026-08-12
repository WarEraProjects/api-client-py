from __future__ import annotations

from typing import Any

from pydantic import AliasChoices, Field

from .common import WareraModel


class WarSide(WareraModel):
    country_id: str | None = Field(default=None, validation_alias=AliasChoices("country"))
    damages: int | None = None
    won_battles_count: int | None = Field(default=None, alias="wonBattlesCount")
    won_rounds_count: int | None = Field(default=None, alias="wonRoundsCount")


class War(WareraModel):
    """War model."""

    attacker: WarSide | None = None
    defender: WarSide | None = None
    battles: list[Any] | None = None
    is_active: bool | None = Field(default=None, alias="isActive")
    priority: str | None = None
    priority_end_at: str | None = Field(default=None, alias="priorityEndAt")
    created_at: str | None = Field(default=None, alias="createdAt")
    updated_at: str | None = Field(default=None, alias="updatedAt")
