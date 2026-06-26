from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import WareraModel


class EquipmentSkills(WareraModel):
    """Stat bonuses granted by an equipped item."""

    attack: float | None = Field(default=None, description="The attack.")
    armor: float | None = Field(default=None, description="The armor.")
    critical_chance: float | None = Field(default=None, description="The critical chance.")
    critical_damages: float | None = Field(default=None, description="The critical damages.")
    dodge: float | None = Field(default=None, description="The dodge.")
    precision: float | None = Field(default=None, description="The precision.")


class Equipment(WareraModel):
    """
    A single equipped item returned by inventory.fetchCurrentEquipment.

    The API returns one object keyed by slot (``weapon``, ``helmet``, ...);
    the resource flattens it into a list of ``Equipment`` with ``slot`` set.
    """

    slot: str | None = Field(default=None, description="The slot.")
    item_id: str | None = Field(default=None, description="The item id.")
    item_code: str | None = Field(default=None, description="The item code.")
    name: str | None = Field(default=None, description="The official name of the country.")
    rarity: str | None = Field(default=None, description="The rarity.")
    stats: dict[str, Any] | None = Field(default=None, description="The stats.")
    # Real per-item fields from the live schema
    type: str | None = Field(default=None, description="The type.")
    code: str | None = Field(default=None, description="The code.")
    skills: EquipmentSkills | None = Field(default=None, description="The skills.")
    state: float | None = Field(default=None, description="The state.")
    max_state: float | None = Field(default=None, description="The max state.")
    quantity: int | None = Field(default=None, description="The quantity.")
    last_acquisition_at: str | None = Field(
        default=None, description="The timestamp of the last acquisition event."
    )
