from __future__ import annotations

from pydantic import AliasChoices, Field

from .common import WareraModel


class BattleRankingEntry(WareraModel):
    rank: int | None = Field(default=None, description="The rank.")
    entity_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices("user", "country", "mu", "entityId", "entity_id"),
    )
    entity_type: str | None = Field(
        default=None, description="The entity type."
    )  # "user" | "country" | "mu"
    name: str | None = Field(default=None, description="The official name of the country.")
    country_id: str | None = Field(
        default=None, validation_alias=AliasChoices("country", "countryId", "country_id")
    )
    value: float | None = Field(
        default=None, description="The value."
    )  # damage / points / money depending on dataType
    side: str | None = Field(default=None, description="The side.")  # "attacker" | "defender"
