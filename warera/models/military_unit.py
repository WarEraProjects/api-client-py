from __future__ import annotations

from .common import WareraModel
from .user import RankingDetail


class MuActiveUpgradeLevels(WareraModel):
    headquarters: int | None = None
    dormitories: int | None = None


class MuRankings(WareraModel):
    mu_weekly_damages: RankingDetail | None = None
    mu_damages: RankingDetail | None = None
    mu_terrain: RankingDetail | None = None
    mu_wealth: RankingDetail | None = None
    mu_bounty: RankingDetail | None = None
    mu_reputation: RankingDetail | None = None


class MuRoles(WareraModel):
    commanders: list[str] | None = None
    managers: list[str] | None = None


class MuLeveling(WareraModel):
    level: int | None = None
    monthly_damages: float | None = None


class MilitaryUnit(WareraModel):
    # NOTE: `id` is inherited from WareraModel with the `_id` alias —
    # do not redeclare it here without the alias or `_id` stops mapping.
    name: str | None = None
    country_id: str | None = None
    owner_id: str | None = None
    members: list[str] | None = None  # API returns a list of member user ID strings
    damage: float | None = None
    terrain: float | None = None
    wealth: float | None = None
    image: str | None = None
    description: str | None = None
    is_recruiting: bool | None = None
    active_upgrade_levels: MuActiveUpgradeLevels | None = None
    avatar_url: str | None = None
    rankings: MuRankings | None = None
    region: str | None = None
    roles: MuRoles | None = None
    user: str | None = None
    leveling: MuLeveling | None = None
    invested_money_by_users: dict[str, float] | None = None
    mercenary_reputation: float | None = None
    last_reputation_buy_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
