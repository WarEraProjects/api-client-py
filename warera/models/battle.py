from typing import Any

from pydantic import AliasChoices, AliasPath, Field

from .common import WareraModel


class BattleSide(WareraModel):
    """Per-side summary (attacker/defender) of a battle."""

    country: str | None = None
    region: str | None = None
    damages: float | None = None
    hit_count: int | None = None
    won_rounds_count: int | None = None
    country_orders: list[str] | None = None
    mu_orders: list[str] | None = None
    money_pool: float | None = None
    money_per_1k_damages: float | None = Field(default=None, alias="moneyPer1kDamages")
    bounty_effective_at: str | None = None


class BattleStats(WareraModel):
    hit_count: int | None = None


class Battle(WareraModel):
    war_id: str | None = Field(
        default=None, validation_alias=AliasChoices("war", "warId", "war_id")
    )
    region_id: str | None = Field(
        default=None, validation_alias=AliasChoices("region", "regionId", "region_id")
    )
    attacker_country_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices(AliasPath("attacker", "country"), "attacker_country_id"),
    )
    defender_country_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices(AliasPath("defender", "country"), "defender_country_id"),
    )
    attacker: BattleSide | None = None
    defender: BattleSide | None = None
    attacker_score: float | None = None
    defender_score: float | None = None
    is_active: bool | None = None
    is_system_resistance: bool | None = None
    is_big_battle: bool | None = None
    winner_country_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices("winner_country", "winnerCountry", "winner_country_id"),
    )
    start_time: str | None = None
    end_time: str | None = None
    current_round: str | int | dict[str, Any] | None = (
        None  # API returns a round ID string, an int, or a full round object
    )
    rounds: list[str] | None = None
    rounds_history: list[Any] | None = None
    rounds_to_win: int | None = None
    total_rounds: int | None = None
    type: str | None = None
    stats: BattleStats | None = None
    created_at: str | None = None
    updated_at: str | None = None


class BattleLive(WareraModel):
    """Response from battle.getLiveBattleData."""

    battle_id: str | None = None
    round_number: int | None = None
    attacker_score: float | None = None
    defender_score: float | None = None
    attacker_damage: float | None = None
    defender_damage: float | None = None
    time_remaining: int | None = None
    is_active: bool | None = None
