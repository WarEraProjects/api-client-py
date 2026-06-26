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
    name: str | None = Field(default=None, description="The official name of the country.")
    scheme: str | None = Field(default=None, description="The scheme.")
    map_accent: str | None = Field(default=None, description="The map accent.")
    leader_id: str | None = Field(default=None, alias="leader")
    member_countries: list[AllianceMemberCountry] | None = Field(
        default=None, description="The member countries."
    )
    current_development: float | int | None = Field(
        default=None, description="The current development."
    )
    core_development: float | int | None = Field(default=None, description="The core development.")
    average_development: float | int | None = Field(
        default=None, description="The average development."
    )
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )
    rankings: AllianceRankings | None = Field(
        default=None, description="The country's current standing in the global leaderboards."
    )
    avatar_url: str | None = Field(
        default=None, description="The CDN URL pointing to the user's profile picture."
    )
