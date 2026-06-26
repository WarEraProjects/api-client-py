from __future__ import annotations

from pydantic import Field

from .common import WareraModel


class TournamentMatchPredecessors(WareraModel):
    attacker: int | None = None
    defender: int | None = None


class TournamentMatch(WareraModel):
    match_index: int | None = None
    predecessors: TournamentMatchPredecessors | None = None
    attacker: str | None = None
    defender: str | None = None
    is_qualification_round: bool | None = None
    battle: str | None = None
    won_by: str | None = None
    possible_attacker_team_ids: list[str] | None = None
    possible_defender_team_ids: list[str] | None = None


class TournamentRound(WareraModel):
    round_number: int | None = None
    cases: float | None = None
    skill_value: float | None = None
    is_qualification_round: bool | None = None
    matches: list[TournamentMatch] = Field(default_factory=list)


class TournamentRegistered(WareraModel):
    countries: list[str] = Field(default_factory=list)
    mus: list[str] = Field(default_factory=list)
    users: list[str] = Field(default_factory=list)


class Tournament(WareraModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    status: str | None = None
    start_at: str | None = None
    # The live API has returned fractional values here — keep this float.
    team_size: float | None = None
    team_count: int | None = None
    rounds_count: int | None = None
    type: str | None = None
    max_rarity: str | None = None
    skill_key: str | None = None
    auto_qualify1st_round: list[str] = Field(default_factory=list, alias="autoQualify1stRound")
    registered: TournamentRegistered | None = None
    active_round: int | None = None
    rounds: dict[str, TournamentRound] = Field(default_factory=dict)
    winner_tournament_team: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class TournamentTeam(WareraModel):
    tournament: str | None = None
    number: int | None = None
    countries: list[str] = Field(default_factory=list)
    mus: list[str] = Field(default_factory=list)
    users: list[str] = Field(default_factory=list)
    participants: list[str] = Field(default_factory=list)
    color_scheme: str | None = None
    estimated_users: int | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
