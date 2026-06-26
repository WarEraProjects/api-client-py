from __future__ import annotations

from typing import Any

from .common import WareraModel


class Event(WareraModel):
    type: str | None = None
    country_id: str | None = None
    countries: list[str] | None = None
    priority: str | int | None = None
    data: dict[str, Any] | None = None
    created_at: str | None = None
    updated_at: str | None = None
    message: str | None = None
