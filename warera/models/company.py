from __future__ import annotations

from typing import Any

from pydantic import AliasChoices, Field

from .common import WareraModel


class CompanyDates(WareraModel):
    pass


class CompanyActiveUpgradeLevels(WareraModel):
    pass


class Company(WareraModel):
    name: str | None = Field(default=None, description="The official name of the country.")
    owner_id: str | None = Field(
        default=None, validation_alias=AliasChoices("owner", "ownerId", "owner_id")
    )
    country_id: str | None = Field(
        default=None, validation_alias=AliasChoices("country", "countryId", "country_id")
    )
    region_id: str | None = Field(
        default=None, validation_alias=AliasChoices("region", "regionId", "region_id")
    )
    type: str | None = Field(default=None, description="The type.")
    quality: int | None = Field(
        default=None,
        description="The quality level (Q1-Q5) of the company determining production efficiency.",
    )
    size: int | None = Field(default=None, description="The size.")
    employees: int | None = Field(default=None, description="The employees.")
    production: float | None = Field(default=None, description="The production.")
    wealth: float | None = Field(default=None, description="The wealth.")
    image: str | None = Field(default=None, description="The image.")
    is_hiring: bool | None = Field(default=None, description="The is hiring.")
    active_upgrade_levels: CompanyActiveUpgradeLevels | None = Field(
        default=None, description="The active upgrade levels."
    )
    concrete_invested: int | float | None = Field(
        default=None, description="The concrete invested."
    )
    dates: CompanyDates | None = Field(default=None, description="The dates.")
    estimated_value: int | float | None = Field(
        default=None, description="The total estimated market value of the company and its assets."
    )
    is_full: bool | None = Field(default=None, description="The is full.")
    item_code: str | None = Field(default=None, description="The item code.")
    moved_up_at: str | None = Field(default=None, description="The moved up at.")
    region: str | None = Field(default=None, description="The UUID of the contested region.")
    user: str | None = Field(default=None, description="The user.")
    worker_count: int | None = Field(default=None, description="The total number of worker.")
    workers: list[Any] | None = Field(default=None, description="The workers.")
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )
