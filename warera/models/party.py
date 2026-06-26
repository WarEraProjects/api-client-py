from __future__ import annotations

from pydantic import AliasChoices, Field

from .common import WareraModel


class PartyEthics(WareraModel):
    """Ethics alignment values for a political party."""

    unethical: bool | None = Field(default=None, description="The unethical.")
    militarism: float | None = Field(default=None, description="The militarism.")
    isolationism: float | None = Field(default=None, description="The isolationism.")
    imperialism: float | None = Field(default=None, description="The imperialism.")
    industrialism: float | None = Field(default=None, description="The industrialism.")


class Party(WareraModel):
    """A political party in WarEra."""

    name: str | None = Field(default=None, description="The official name of the country.")
    description: str | None = Field(default=None, description="The description.")
    country: str | None = Field(
        default=None, description="The UUID of the country this user holds citizenship in."
    )
    country_id: str | None = Field(
        default=None, validation_alias=AliasChoices("country", "countryId", "country_id")
    )
    region: str | None = Field(default=None, description="The UUID of the contested region.")
    region_id: str | None = Field(
        default=None, validation_alias=AliasChoices("region", "regionId", "region_id")
    )
    leader: str | None = Field(default=None, description="The leader.")
    leader_id: str | None = Field(
        default=None, validation_alias=AliasChoices("leader", "leaderId", "leader_id")
    )
    council_members: list[str] | None = Field(default=None, description="The council members.")
    members: list[str] | None = Field(default=None, description="The members.")
    ethics: PartyEthics | None = Field(default=None, description="The ethics.")
    avatar_url: str | None = Field(
        default=None, description="The CDN URL pointing to the user's profile picture."
    )
    treasurer: str | None = Field(default=None, description="The treasurer.")
    primary_winner: str | None = Field(default=None, description="The primary winner.")
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )
