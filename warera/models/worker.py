from __future__ import annotations

from pydantic import Field

from .common import WareraModel


class Worker(WareraModel):
    user_id: str | None = Field(default=None, description="The user id.")
    company_id: str | None = Field(default=None, description="The company id.")
    salary: float | None = Field(default=None, description="The salary.")
    started_at: str | None = Field(default=None, description="The started at.")


class WorkerCount(WareraModel):
    user_id: str | None = Field(default=None, description="The user id.")
    total: int | None = Field(default=None, description="The total.")
