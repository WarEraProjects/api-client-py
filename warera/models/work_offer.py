from __future__ import annotations

from pydantic import Field

from .common import WareraModel


class WorkOffer(WareraModel):
    company_id: str | None = Field(default=None, description="The company id.")
    region_id: str | None = Field(default=None, description="The region id.")
    salary: float | None = Field(default=None, description="The salary.")
    energy: float | None = Field(default=None, description="The energy.")
    production: float | None = Field(default=None, description="The production.")
    citizenship: str | None = Field(default=None, description="The citizenship.")
    positions: int | None = Field(default=None, description="The positions.")
    filled: int | None = Field(default=None, description="The filled.")
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
