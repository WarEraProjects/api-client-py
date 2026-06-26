from __future__ import annotations

from pydantic import AliasChoices, Field

from .common import WareraModel
from .inventory import Equipment


class Hit(WareraModel):
    """A single hit entry (round.getLastHits / round side lastHits)."""

    user: str | None = Field(default=None, description="The user.")
    mu: str | None = Field(
        default=None, description="The UUID of the Military Unit this user belongs to."
    )
    damages: float | None = Field(default=None, description="The damages.")
    is_critical_hit: bool | None = Field(default=None, description="The is critical hit.")
    is_missed: bool | None = Field(default=None, description="The is missed.")
    hit_at: str | None = Field(default=None, description="The hit at.")
    ammo: str | None = Field(default=None, description="The ammo.")
    weapon: Equipment | None = Field(default=None, description="The weapon.")
    equipments: list[Equipment] | None = Field(default=None, description="The equipments.")


class RoundSide(WareraModel):
    """Combat stats of one side (attacker/defender) within a round."""

    country: str | None = Field(
        default=None, description="The UUID of the country this user holds citizenship in."
    )
    damages: float | None = Field(default=None, description="The damages.")
    points: float | None = Field(default=None, description="The points.")
    hit_count: int | None = Field(default=None, description="The total number of hit.")
    last_hits: list[Hit] | None = Field(
        default=None, description="The timestamp of the last hits event."
    )


class RoundLive(WareraModel):
    ticks_count: int | None = Field(default=None, description="The total number of ticks.")
    actual_tick_points: float | None = Field(default=None, description="The actual tick points.")
    next_tick_at: str | None = Field(default=None, description="The next tick at.")


class Round(WareraModel):
    battle_id: str | None = Field(
        default=None, validation_alias=AliasChoices("battle", "battleId", "battle_id")
    )
    round_number: int | None = Field(
        default=None, validation_alias=AliasChoices("number", "roundNumber", "round_number")
    )
    is_active: bool | None = Field(
        default=None,
        description="Whether the user has logged in recently and is considered an active player.",
    )
    attacker: RoundSide | None = Field(
        default=None, description="The UUID of the country initiating the battle."
    )
    defender: RoundSide | None = Field(
        default=None, description="The UUID of the country defending the region."
    )
    live: RoundLive | None = Field(default=None, description="The live.")
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )
