from __future__ import annotations

from typing import Any

from pydantic import Field

from .common import WareraModel


class BattleLootPoolItem(WareraModel):
    item: dict[str, Any]  # RoundWeapon = Field(description="The item.")
    pool: str = Field(description="The pool.")
    rank: int = Field(description="The rank.")
    round: str | None = Field(default=None, description="The round.")


class BattleLootSummary(WareraModel):
    v: int | None = Field(default=None, description="The v.")  # __v
    battle: str = Field(description="The battle.")
    case1_count: int = Field(description="The total number of case1.")
    case2_count: int = Field(description="The total number of case2.")
    created_at: str = Field(description="The timestamp when this record was created.")
    hits: int = Field(description="The hits.")
    pool_loot: list[BattleLootPoolItem] = Field(description="The pool loot.")
    total_dmg: int = Field(description="The total dmg.")
    total_money_from_bounty: int = Field(description="The total money from bounty.")
    total_money_from_contract: int = Field(description="The total money from contract.")
    updated_at: str = Field(description="The timestamp when this record was last modified.")
    user: str = Field(description="The user.")
