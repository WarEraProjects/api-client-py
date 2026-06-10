from __future__ import annotations

from .common import WareraModel
from .user import RankingDetail


class CountryTaxes(WareraModel):
    income: float | None = None
    market: float | None = None
    self_work: float | None = None


class CountryUnrest(WareraModel):
    bar: float | None = None
    bar_max: float | None = None
    last_contribution_at: str | None = None


class CountryStrategicResourceMap(WareraModel):
    """Region IDs holding each strategic resource."""

    coal: list[str] | None = None
    diamonds: list[str] | None = None
    gold: list[str] | None = None
    lithium: list[str] | None = None
    rare_earths: list[str] | None = None
    uranium: list[str] | None = None


class CountryStrategicBonuses(WareraModel):
    production_percent: float | None = None
    development_percent: float | None = None


class CountryStrategicResources(WareraModel):
    resources: CountryStrategicResourceMap | None = None
    bonuses: CountryStrategicBonuses | None = None


class CountryRankings(WareraModel):
    country_region_diff: RankingDetail | None = None
    country_damages: RankingDetail | None = None
    weekly_country_damages: RankingDetail | None = None
    weekly_country_damages_per_citizen: RankingDetail | None = None
    country_development: RankingDetail | None = None
    country_active_population: RankingDetail | None = None
    country_wealth: RankingDetail | None = None
    country_bounty: RankingDetail | None = None
    country_production_bonus: RankingDetail | None = None


class Country(WareraModel):
    name: str | None = None
    code: str | None = None
    money: float | None = None
    scheme: str | None = None
    map_accent: str | None = None
    discord_url: str | None = None
    specialized_item: str | None = None
    pinned_article: str | None = None
    current_battle_order: str | None = None
    ruling_party: str | None = None
    alliance_id: str | None = None
    enemy: str | None = None
    # Relations
    allies: list[str] | None = None
    wars_with: list[str] | None = None
    defensive_pacts: list[str] | None = None
    orgs: list[str] | None = None
    non_aggression_until: dict[str, str] | None = None
    # Development / population
    development: float | None = None
    current_development: float | None = None
    average_development: float | None = None
    core_development: float | None = None
    current_population: int | None = None
    # Nested structures
    taxes: CountryTaxes | None = None
    unrest: CountryUnrest | None = None
    strategic_resources: CountryStrategicResources | None = None
    rankings: CountryRankings | None = None
    created_at: str | None = None
    updated_at: str | None = None
