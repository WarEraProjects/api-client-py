from __future__ import annotations

from pydantic import Field

from .common import WareraModel
from .user import RankingDetail


class MuActiveUpgradeLevels(WareraModel):
    headquarters: int | None = Field(default=None, description="The headquarters.")
    dormitories: int | None = Field(default=None, description="The dormitories.")


class MuRankings(WareraModel):
    mu_weekly_damages: RankingDetail | None = Field(
        default=None, description="The mu weekly damages."
    )
    mu_damages: RankingDetail | None = Field(default=None, description="The mu damages.")
    mu_terrain: RankingDetail | None = Field(default=None, description="The mu terrain.")
    mu_wealth: RankingDetail | None = Field(default=None, description="The mu wealth.")
    mu_bounty: RankingDetail | None = Field(default=None, description="The mu bounty.")
    mu_reputation: RankingDetail | None = Field(default=None, description="The mu reputation.")


class MuRoles(WareraModel):
    commanders: list[str] | None = Field(default=None, description="The commanders.")
    managers: list[str] | None = Field(default=None, description="The managers.")


class MuLeveling(WareraModel):
    level: int | None = Field(default=None, description="The current overall level of the entity.")
    monthly_damages: float | None = Field(default=None, description="The monthly damages.")


class MilitaryUnit(WareraModel):
    # NOTE: `id` is inherited from WareraModel with the `_id` alias —
    # do not redeclare it here without the alias or `_id` stops mapping.
    name: str | None = Field(default=None, description="The official name of the country.")
    country_id: str | None = Field(default=None, description="The country id.")
    owner_id: str | None = Field(default=None, description="The owner id.")
    members: list[str] | None = Field(
        default=None, description="The members. API returns a list of member user ID strings."
    )
    damage: float | None = Field(default=None, description="The damage.")
    terrain: float | None = Field(default=None, description="The terrain.")
    wealth: float | None = Field(default=None, description="The wealth.")
    image: str | None = Field(default=None, description="The image.")
    description: str | None = Field(default=None, description="The description.")
    is_recruiting: bool | None = Field(default=None, description="The is recruiting.")
    active_upgrade_levels: MuActiveUpgradeLevels | None = Field(
        default=None, description="The active upgrade levels."
    )
    avatar_url: str | None = Field(
        default=None, description="The CDN URL pointing to the user's profile picture."
    )
    rankings: MuRankings | None = Field(
        default=None, description="The country's current standing in the global leaderboards."
    )
    region: str | None = Field(default=None, description="The UUID of the contested region.")
    roles: MuRoles | None = Field(default=None, description="The roles.")
    user: str | None = Field(default=None, description="The user.")
    leveling: MuLeveling | None = Field(default=None, description="The leveling.")
    invested_money_by_users: dict[str, float] | None = Field(
        default=None, description="The invested money by users."
    )
    mercenary_reputation: float | None = Field(
        default=None, description="The mercenary reputation."
    )
    last_reputation_buy_at: str | None = Field(
        default=None, description="The timestamp of the last reputation buy event."
    )
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )
