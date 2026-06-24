from __future__ import annotations

from pydantic import Field

from warera.models.common import ReprMixin, WareraModel


class AllianceRankingEntry(ReprMixin, WareraModel):
    value: float | int | None = None
    rank: int | None = None
    tier: str | None = None


class AllianceRankings(ReprMixin, WareraModel):
    alliance_initial_development: AllianceRankingEntry | None = None
    alliance_development: AllianceRankingEntry | None = None
    alliance_weekly_damages: AllianceRankingEntry | None = None
    alliance_damages: AllianceRankingEntry | None = None
    alliance_population: AllianceRankingEntry | None = None
    alliance_weekly_damages_per_citizen: AllianceRankingEntry | None = None


class AllianceMemberCountry(ReprMixin, WareraModel):
    country_id: str | None = Field(default=None, alias="country")
    core_development: float | int | None = None
    average_development: float | int | None = None
    suspended: bool | None = None


class Alliance(WareraModel):
    name: str | None = None
    scheme: str | None = None
    map_accent: str | None = None
    leader_id: str | None = Field(default=None, alias="leader")
    member_countries: list[AllianceMemberCountry] | None = None
    current_development: float | int | None = None
    core_development: float | int | None = None
    average_development: float | int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    rankings: AllianceRankings | None = None
    avatar_url: str | None = None
