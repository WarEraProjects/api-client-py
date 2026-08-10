from __future__ import annotations

from pydantic import AliasChoices, Field

from .common import WareraModel


class Worker(WareraModel):
    user_id: str | None = Field(
        default=None, validation_alias=AliasChoices("user", "userId", "user_id")
    )
    company_id: str | None = Field(
        default=None, validation_alias=AliasChoices("company", "companyId", "company_id")
    )
    employer_id: str | None = Field(
        default=None, validation_alias=AliasChoices("employer", "employerId", "employer_id")
    )
    salary: float | None = Field(
        default=None, validation_alias=AliasChoices("wage", "salary")
    )
    started_at: str | None = Field(
        default=None, validation_alias=AliasChoices("joinedAt", "startedAt", "started_at")
    )
    fidelity: int | None = None
    last_fidelity_increase_at: str | None = None


class WorkerCount(WareraModel):
    user_id: str | None = None
    total: int | None = None
