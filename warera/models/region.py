from __future__ import annotations

from pydantic import Field

from .battle import Battle
from .common import WareraModel


class RegionStats(WareraModel):
    invested_money: float | None = Field(default=None, description="The invested money.")


class RegionDates(WareraModel):
    last_ownership_change_at: str | None = Field(
        default=None, description="The timestamp of the last ownership change event."
    )


class RegionActiveUpgradeLevels(WareraModel):
    base: int | None = Field(default=None, description="The base.")
    bunker: int | None = Field(default=None, description="The bunker.")
    pacification_center: int | None = Field(default=None, description="The pacification center.")


class RegionDeposit(WareraModel):
    type: str | None = Field(default=None, description="The type.")
    bonus_percent: float | None = Field(default=None, description="The bonus percent.")
    starts_at: str | None = Field(default=None, description="The starts at.")
    ends_at: str | None = Field(default=None, description="The ends at.")


class RegionUpgradeConstruction(WareraModel):
    """One contribution entry in an upgrade's construction history."""

    construction: float | None = Field(default=None, description="The construction.")
    construction_at: str | None = Field(default=None, description="The construction at.")
    user: str | None = Field(default=None, description="The user.")


class RegionUpgrade(WareraModel):
    """State of a single region upgrade (base, bunker, ...)."""

    level: int | None = Field(default=None, description="The current overall level of the entity.")
    status: str | None = Field(default=None, description="The status.")
    status_changed_at: str | None = Field(default=None, description="The status changed at.")
    construction_points: float | None = Field(default=None, description="The construction points.")
    invested_money: float | None = Field(default=None, description="The invested money.")
    is_under_construction: bool | None = Field(
        default=None, description="The is under construction."
    )
    construction_started_at: str | None = Field(
        default=None, description="The construction started at."
    )
    construction_ended_at: str | None = Field(
        default=None, description="The construction ended at."
    )
    last_constructions: list[RegionUpgradeConstruction] | None = Field(
        default=None, description="The timestamp of the last constructions event."
    )


class RegionUpgradesV2(WareraModel):
    upgrades: dict[str, RegionUpgrade] | None = Field(default=None, description="The upgrades.")
    active_construction_count: int | None = Field(
        default=None, description="The total number of active construction."
    )


class Region(WareraModel):
    name: str | None = Field(default=None, description="The official name of the country.")
    code: str | None = Field(default=None, description="The code.")
    main_city: str | None = Field(default=None, description="The main city.")
    country: str | None = Field(
        default=None, description="The UUID of the country this user holds citizenship in."
    )
    country_code: str | None = Field(default=None, description="The country code.")
    initial_country: str | None = Field(default=None, description="The initial country.")
    is_capital: bool | None = Field(default=None, description="The is capital.")
    is_linked_to_capital: bool | None = Field(default=None, description="The is linked to capital.")
    has_coast: bool | None = Field(default=None, description="The has coast.")
    biome: str | None = Field(default=None, description="The biome.")
    climate: str | None = Field(default=None, description="The climate.")
    position: list[float] | None = Field(default=None, description="The position.")
    neighbors: list[str] | None = Field(default=None, description="The neighbors.")
    development: float | None = Field(default=None, description="The development.")
    base_development: float | None = Field(default=None, description="The base development.")
    current_population: int | None = Field(default=None, description="The current population.")
    resistance: float | None = Field(default=None, description="The resistance.")
    resistance_max: float | None = Field(default=None, description="The resistance max.")
    strategic_resource: str | None = Field(default=None, description="The strategic resource.")
    deposit: RegionDeposit | None = Field(default=None, description="The deposit.")
    stats: RegionStats | None = Field(default=None, description="The stats.")
    dates: RegionDates | None = Field(default=None, description="The dates.")
    active_upgrade_levels: RegionActiveUpgradeLevels | None = Field(
        default=None, description="The active upgrade levels."
    )
    upgrades_v2: RegionUpgradesV2 | None = Field(default=None, description="The upgrades v2.")
    # Full battle object when a battle is active on this region.
    active_battle: Battle | None = Field(default=None, description="The active battle.")
    last_battle_ended_at: str | None = Field(
        default=None, description="The timestamp of the last battle ended event."
    )
    last_resistance_contribution_at: str | None = Field(
        default=None, description="The timestamp of the last resistance contribution event."
    )
    last_revolt_ended_at: str | None = Field(
        default=None, description="The timestamp of the last revolt ended event."
    )
