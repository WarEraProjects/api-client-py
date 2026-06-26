from typing import Any

from pydantic import AliasChoices, AliasPath, Field

from .common import WareraModel


class BattleSide(WareraModel):
    """Per-side summary (attacker/defender) of a battle."""

    country: str | None = Field(default=None, description="The UUID of the country this user holds citizenship in.")
    region: str | None = Field(default=None, description="The UUID of the contested region.")
    damages: float | None = Field(default=None, description="The damages.")
    hit_count: int | None = Field(default=None, description="The total number of hit.")
    won_rounds_count: int | None = Field(default=None, description="The total number of won rounds.")
    country_orders: list[str] | None = Field(default=None, description="The country orders.")
    mu_orders: list[str] | None = Field(default=None, description="The mu orders.")
    money_pool: float | None = Field(default=None, description="The money pool.")
    money_per_1k_damages: float | None = Field(default=None, alias="moneyPer1kDamages")
    bounty_effective_at: str | None = Field(default=None, description="The bounty effective at.")


class BattleStats(WareraModel):
    hit_count: int | None = Field(default=None, description="The total number of hit.")


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
    attacker: BattleSide | None = Field(default=None, description="The UUID of the country initiating the battle.")
    defender: BattleSide | None = Field(default=None, description="The UUID of the country defending the region.")
    attacker_score: float | None = Field(default=None, description="The attacker score.")
    defender_score: float | None = Field(default=None, description="The defender score.")
    is_active: bool | None = Field(default=None, description="Whether the user has logged in recently and is considered an active player.")
    is_system_resistance: bool | None = Field(default=None, description="The is system resistance.")
    is_big_battle: bool | None = Field(default=None, description="The is big battle.")
    winner_country_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices("winner_country", "winnerCountry", "winner_country_id"),
    )
    start_time: str | None = Field(default=None, description="The start time.")
    end_time: str | None = Field(default=None, description="The end time.")
    current_round: str | int | dict[str, Any] | None = Field(default=None, description="The current round. API returns a round ID string, an int, or a full round object.")
    rounds: list[str] | None = Field(default=None, description="The rounds.")
    rounds_history: list[Any] | None = Field(default=None, description="The rounds history.")
    rounds_to_win: int | None = Field(default=None, description="The rounds to win.")
    total_rounds: int | None = Field(default=None, description="The total rounds.")
    type: str | None = Field(default=None, description="The type.")
    stats: BattleStats | None = Field(default=None, description="The stats.")
    created_at: str | None = Field(default=None, description="The timestamp when this record was created.")
    updated_at: str | None = Field(default=None, description="The timestamp when this record was last modified.")


class BattleLive(WareraModel):
    """Response from battle.getLiveBattleData."""

    battle_id: str | None = Field(default=None, description="The battle id.")
    round_number: int | None = Field(default=None, description="The round number.")
    attacker_score: float | None = Field(default=None, description="The attacker score.")
    defender_score: float | None = Field(default=None, description="The defender score.")
    attacker_damage: float | None = Field(default=None, description="The attacker damage.")
    defender_damage: float | None = Field(default=None, description="The defender damage.")
    time_remaining: int | None = Field(default=None, description="The time remaining.")
    is_active: bool | None = Field(default=None, description="Whether the user has logged in recently and is considered an active player.")
