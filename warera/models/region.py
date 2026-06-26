from __future__ import annotations

from .battle import Battle
from .common import WareraModel


class RegionStats(WareraModel):
    invested_money: float | None = None


class RegionDates(WareraModel):
    last_ownership_change_at: str | None = None


class RegionActiveUpgradeLevels(WareraModel):
    base: int | None = None
    bunker: int | None = None
    pacification_center: int | None = None


class RegionDeposit(WareraModel):
    type: str | None = None
    bonus_percent: float | None = None
    starts_at: str | None = None
    ends_at: str | None = None


class RegionUpgradeConstruction(WareraModel):
    """One contribution entry in an upgrade's construction history."""

    construction: float | None = None
    construction_at: str | None = None
    user: str | None = None


class RegionUpgrade(WareraModel):
    """State of a single region upgrade (base, bunker, ...)."""

    level: int | None = None
    status: str | None = None
    status_changed_at: str | None = None
    construction_points: float | None = None
    invested_money: float | None = None
    is_under_construction: bool | None = None
    construction_started_at: str | None = None
    construction_ended_at: str | None = None
    last_constructions: list[RegionUpgradeConstruction] | None = None


class RegionUpgradesV2(WareraModel):
    upgrades: dict[str, RegionUpgrade] | None = None
    active_construction_count: int | None = None


class Region(WareraModel):
    name: str | None = None
    code: str | None = None
    main_city: str | None = None
    country: str | None = None
    country_code: str | None = None
    initial_country: str | None = None
    is_capital: bool | None = None
    is_linked_to_capital: bool | None = None
    has_coast: bool | None = None
    biome: str | None = None
    climate: str | None = None
    position: list[float] | None = None
    neighbors: list[str] | None = None
    development: float | None = None
    base_development: float | None = None
    current_population: int | None = None
    resistance: float | None = None
    resistance_max: float | None = None
    strategic_resource: str | None = None
    deposit: RegionDeposit | None = None
    stats: RegionStats | None = None
    dates: RegionDates | None = None
    active_upgrade_levels: RegionActiveUpgradeLevels | None = None
    upgrades_v2: RegionUpgradesV2 | None = None
    # Full battle object when a battle is active on this region.
    active_battle: Battle | None = None
    last_battle_ended_at: str | None = None
    last_resistance_contribution_at: str | None = None
    last_revolt_ended_at: str | None = None
