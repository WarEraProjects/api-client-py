from __future__ import annotations

from pydantic import AliasChoices, Field

from .common import WareraModel
from .inventory import Equipment


class Hit(WareraModel):
    """A single hit entry (round.getLastHits / round side lastHits)."""

    user: str | None = None
    mu: str | None = None
    damages: float | None = None
    is_critical_hit: bool | None = None
    is_missed: bool | None = None
    hit_at: str | None = None
    ammo: str | None = None
    weapon: Equipment | None = None
    equipments: list[Equipment] | None = None


class RoundSide(WareraModel):
    """Combat stats of one side (attacker/defender) within a round."""

    country: str | None = None
    damages: float | None = None
    points: float | None = None
    hit_count: int | None = None
    last_hits: list[Hit] | None = None


class RoundLive(WareraModel):
    ticks_count: int | None = None
    actual_tick_points: float | None = None
    next_tick_at: str | None = None


class Round(WareraModel):
    battle_id: str | None = Field(
        default=None, validation_alias=AliasChoices("battle", "battleId", "battle_id")
    )
    round_number: int | None = Field(
        default=None, validation_alias=AliasChoices("number", "roundNumber", "round_number")
    )
    is_active: bool | None = None
    attacker: RoundSide | None = None
    defender: RoundSide | None = None
    live: RoundLive | None = None
    created_at: str | None = None
    updated_at: str | None = None
