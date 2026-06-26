from __future__ import annotations

from pydantic import Field

from .common import WareraModel
from .user import RankingDetail


class CountryTaxes(WareraModel):
    income: float | None = Field(default=None, description="The income.")
    market: float | None = Field(default=None, description="The market.")
    self_work: float | None = Field(
        default=None, description="The tax rate applied when a user works for their own companies."
    )


class CountryUnrest(WareraModel):
    bar: float | None = Field(default=None, description="The bar.")
    bar_max: float | None = Field(default=None, description="The bar max.")
    last_contribution_at: str | None = Field(
        default=None, description="The timestamp of the last contribution event."
    )


class CountryStrategicResourceMap(WareraModel):
    """Region IDs holding each strategic resource."""

    coal: list[str] | None = Field(default=None, description="The coal.")
    diamonds: list[str] | None = Field(default=None, description="The diamonds.")
    gold: list[str] | None = Field(default=None, description="The gold.")
    lithium: list[str] | None = Field(default=None, description="The lithium.")
    rare_earths: list[str] | None = Field(default=None, description="The rare earths.")
    uranium: list[str] | None = Field(default=None, description="The uranium.")


class CountryStrategicBonuses(WareraModel):
    production_percent: float | None = Field(default=None, description="The production percent.")
    development_percent: float | None = Field(default=None, description="The development percent.")


class CountryStrategicResources(WareraModel):
    resources: CountryStrategicResourceMap | None = Field(
        default=None, description="The resources."
    )
    bonuses: CountryStrategicBonuses | None = Field(default=None, description="The bonuses.")


class CountryRankings(WareraModel):
    country_region_diff: RankingDetail | None = Field(
        default=None, description="The country region diff."
    )
    country_damages: RankingDetail | None = Field(default=None, description="The country damages.")
    weekly_country_damages: RankingDetail | None = Field(
        default=None, description="The weekly country damages."
    )
    weekly_country_damages_per_citizen: RankingDetail | None = Field(
        default=None, description="The weekly country damages per citizen."
    )
    country_development: RankingDetail | None = Field(
        default=None, description="The country development."
    )
    country_active_population: RankingDetail | None = Field(
        default=None, description="The country active population."
    )
    country_wealth: RankingDetail | None = Field(default=None, description="The country wealth.")
    country_bounty: RankingDetail | None = Field(default=None, description="The country bounty.")
    country_production_bonus: RankingDetail | None = Field(
        default=None, description="The country production bonus."
    )


class Country(WareraModel):
    name: str | None = Field(default=None, description="The official name of the country.")
    code: str | None = Field(default=None, description="The code.")
    money: float | None = Field(default=None, description="The money.")
    scheme: str | None = Field(default=None, description="The scheme.")
    map_accent: str | None = Field(default=None, description="The map accent.")
    discord_url: str | None = Field(default=None, description="The discord url.")
    specialized_item: str | None = Field(default=None, description="The specialized item.")
    pinned_article: str | None = Field(default=None, description="The pinned article.")
    current_battle_order: str | None = Field(default=None, description="The current battle order.")
    ruling_party: str | None = Field(default=None, description="The ruling party.")
    alliance_id: str | None = Field(default=None, description="The alliance id.")
    enemy: str | None = Field(default=None, description="The enemy.")
    # Relations
    allies: list[str] | None = Field(
        default=None,
        description="A list of country UUIDs that share a Mutual Protection Pact (MPP) with this country.",
    )
    wars_with: list[str] | None = Field(
        default=None, description="A list of country UUIDs this country is currently at war with."
    )
    defensive_pacts: list[str] | None = Field(
        default=None, description="A list of country UUIDs offering defensive guarantees."
    )
    orgs: list[str] | None = Field(default=None, description="The orgs.")
    non_aggression_until: dict[str, str] | None = Field(
        default=None, description="The non aggression until."
    )
    # Development / population
    development: float | None = Field(default=None, description="The development.")
    current_development: float | None = Field(default=None, description="The current development.")
    average_development: float | None = Field(default=None, description="The average development.")
    core_development: float | None = Field(default=None, description="The core development.")
    current_population: int | None = Field(default=None, description="The current population.")
    # Nested structures
    taxes: CountryTaxes | None = Field(
        default=None,
        description="The various tax rates applied to economic activities within the country.",
    )
    unrest: CountryUnrest | None = Field(default=None, description="The unrest.")
    strategic_resources: CountryStrategicResources | None = Field(
        default=None, description="The strategic resources."
    )
    rankings: CountryRankings | None = Field(
        default=None, description="The country's current standing in the global leaderboards."
    )
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )
