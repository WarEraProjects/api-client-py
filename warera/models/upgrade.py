from __future__ import annotations

from pydantic import AliasChoices, Field

from .common import WareraModel


class Upgrade(WareraModel):
    upgrade_type: str | None = None
    level: int | None = None
    status: str | None = None
    status_changed_at: str | None = None
    region_id: str | None = Field(
        default=None, validation_alias=AliasChoices("region", "regionId", "region_id")
    )
    company_id: str | None = Field(
        default=None, validation_alias=AliasChoices("company", "companyId", "company_id")
    )
    mu_id: str | None = Field(default=None, validation_alias=AliasChoices("mu", "muId", "mu_id"))
    invested_money: float | None = None
    invested_concrete: float | None = None
    invested_steel: float | None = None
    dependant_users_count: int | None = None
    last_upgrade_at: str | None = None
    last_downgrade_at: str | None = None
    will_be_active_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
