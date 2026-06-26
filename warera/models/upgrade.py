from __future__ import annotations

from pydantic import AliasChoices, Field

from .common import WareraModel


class Upgrade(WareraModel):
    upgrade_type: str | None = Field(default=None, description="The upgrade type.")
    level: int | None = Field(default=None, description="The current overall level of the entity.")
    status: str | None = Field(default=None, description="The status.")
    status_changed_at: str | None = Field(default=None, description="The status changed at.")
    region_id: str | None = Field(
        default=None, validation_alias=AliasChoices("region", "regionId", "region_id")
    )
    company_id: str | None = Field(
        default=None, validation_alias=AliasChoices("company", "companyId", "company_id")
    )
    mu_id: str | None = Field(default=None, validation_alias=AliasChoices("mu", "muId", "mu_id"))
    invested_money: float | None = Field(default=None, description="The invested money.")
    invested_concrete: float | None = Field(default=None, description="The invested concrete.")
    invested_steel: float | None = Field(default=None, description="The invested steel.")
    dependant_users_count: int | None = Field(
        default=None, description="The total number of dependant users."
    )
    last_upgrade_at: str | None = Field(
        default=None, description="The timestamp of the last upgrade event."
    )
    last_downgrade_at: str | None = Field(
        default=None, description="The timestamp of the last downgrade event."
    )
    will_be_active_at: str | None = Field(default=None, description="The will be active at.")
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )
