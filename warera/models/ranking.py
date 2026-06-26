from pydantic import AliasChoices, Field

from .common import WareraModel


class RankingEntry(WareraModel):
    rank: int | None = Field(default=None, description="The rank.")
    entity_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices("user", "country", "mu", "entityId", "entity_id"),
    )
    name: str | None = Field(default=None, description="The official name of the country.")
    country_id: str | None = Field(
        default=None, validation_alias=AliasChoices("country", "countryId", "country_id")
    )
    value: float | None = Field(default=None, description="The value.")
    tier: str | None = Field(default=None, description="The tier.")
    user: str | None = Field(default=None, description="The user.")
    mu: str | None = Field(
        default=None, description="The UUID of the Military Unit this user belongs to."
    )
    image: str | None = Field(default=None, description="The image.")
