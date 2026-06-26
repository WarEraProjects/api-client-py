from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import WareraModel


class ActionLog(WareraModel):
    """A single action log entry from actionLog.getPaginated."""

    user_id: str | None = Field(default=None, description="The user id.")
    mu_id: str | None = Field(default=None, description="The mu id.")
    country_id: str | None = Field(default=None, description="The country id.")
    action_type: str | None = Field(default=None, description="The action type.")
    timestamp: str | None = Field(default=None, description="The timestamp.")
    details: dict[str, Any] | None = Field(default=None, description="The details.")
