from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import WareraModel


class Event(WareraModel):
    type: str | None = Field(default=None, description="The type.")
    country_id: str | None = Field(default=None, description="The country id.")
    countries: list[str] | None = Field(default=None, description="The countries.")
    priority: str | int | None = Field(default=None, description="The priority.")
    data: dict[str, Any] | None = Field(default=None, description="The data.")
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )
    message: str | None = Field(default=None, description="The message.")
