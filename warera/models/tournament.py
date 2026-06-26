from __future__ import annotations

from pydantic import Field

from .common import WareraModel


class TournamentMatchPredecessors(WareraModel):
    attacker: int | None = Field(
        default=None, description="The UUID of the country initiating the battle."
    )
    defender: int | None = Field(
        default=None, description="The UUID of the country defending the region."
    )


class TournamentMatch(WareraModel):
    match_index: int | None = Field(default=None, description="The match index.")
    predecessors: TournamentMatchPredecessors | None = Field(
        default=None, description="The predecessors."
    )
    attacker: str | None = Field(
        default=None, description="The UUID of the country initiating the battle."
    )
    defender: str | None = Field(
        default=None, description="The UUID of the country defending the region."
    )
    is_qualification_round: bool | None = Field(
        default=None, description="The is qualification round."
    )
    battle: str | None = Field(default=None, description="The battle.")
    won_by: str | None = Field(default=None, description="The won by.")
    possible_attacker_team_ids: list[str] | None = Field(
        default=None, description="The possible attacker team ids."
    )
    possible_defender_team_ids: list[str] | None = Field(
        default=None, description="The possible defender team ids."
    )


class TournamentRound(WareraModel):
    round_number: int | None = Field(default=None, description="The round number.")
    cases: float | None = Field(default=None, description="The cases.")
    skill_value: float | None = Field(default=None, description="The skill value.")
    is_qualification_round: bool | None = Field(
        default=None, description="The is qualification round."
    )
    matches: list[TournamentMatch] = Field(default_factory=list)


class TournamentRegistered(WareraModel):
    countries: list[str] = Field(default_factory=list)
    mus: list[str] = Field(default_factory=list)
    users: list[str] = Field(default_factory=list)


class Tournament(WareraModel):
    name: str | None = Field(default=None, description="The official name of the country.")
    description: str | None = Field(default=None, description="The description.")
    is_active: bool | None = Field(
        default=None,
        description="Whether the user has logged in recently and is considered an active player.",
    )
    status: str | None = Field(default=None, description="The status.")
    start_at: str | None = Field(
        default=None, description="The timestamp when the battle officially commenced."
    )
    # The live API has returned fractional values here — keep this float.
    team_size: float | None = Field(default=None, description="The team size.")
    team_count: int | None = Field(default=None, description="The total number of team.")
    rounds_count: int | None = Field(default=None, description="The total number of rounds.")
    type: str | None = Field(default=None, description="The type.")
    max_rarity: str | None = Field(default=None, description="The max rarity.")
    skill_key: str | None = Field(default=None, description="The skill key.")
    auto_qualify1st_round: list[str] = Field(default_factory=list, alias="autoQualify1stRound")
    registered: TournamentRegistered | None = Field(default=None, description="The registered.")
    active_round: int | None = Field(default=None, description="The active round.")
    rounds: dict[str, TournamentRound] = Field(default_factory=dict)
    winner_tournament_team: str | None = Field(
        default=None, description="The winner tournament team."
    )
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )


class TournamentTeam(WareraModel):
    tournament: str | None = Field(default=None, description="The tournament.")
    number: int | None = Field(default=None, description="The number.")
    countries: list[str] = Field(default_factory=list)
    mus: list[str] = Field(default_factory=list)
    users: list[str] = Field(default_factory=list)
    participants: list[str] = Field(default_factory=list)
    color_scheme: str | None = Field(default=None, description="The color scheme.")
    estimated_users: int | None = Field(default=None, description="The estimated users.")
    status: str | None = Field(default=None, description="The status.")
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )
