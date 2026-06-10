from __future__ import annotations

from typing import Any

from .common import WareraModel


class EquipmentSkills(WareraModel):
    """Stat bonuses granted by an equipped item."""

    attack: float | None = None
    armor: float | None = None
    critical_chance: float | None = None
    critical_damages: float | None = None
    dodge: float | None = None
    precision: float | None = None


class Equipment(WareraModel):
    """
    A single equipped item returned by inventory.fetchCurrentEquipment.

    The API returns one object keyed by slot (``weapon``, ``helmet``, ...);
    the resource flattens it into a list of ``Equipment`` with ``slot`` set.
    """

    slot: str | None = None
    item_id: str | None = None
    item_code: str | None = None
    name: str | None = None
    rarity: str | None = None
    stats: dict[str, Any] | None = None
    # Real per-item fields from the live schema
    type: str | None = None
    code: str | None = None
    skills: EquipmentSkills | None = None
    state: float | None = None
    max_state: float | None = None
    quantity: int | None = None
    last_acquisition_at: str | None = None
