from __future__ import annotations

from pydantic import Field

from .common import WareraModel


class MercenaryContractAuctionBid(WareraModel):
    bid_at: str = Field(description="The bid at.")
    mu: str = Field(description="The UUID of the Military Unit this user belongs to.")
    payout: int | float = Field(description="The payout.")
    per_k: int | float = Field(description="The per k.")
    user: str = Field(description="The user.")


class MercenaryContractAuction(WareraModel):
    v: int | None = Field(default=None, alias="__v")
    battle: str = Field(description="The battle.")
    bids: list[MercenaryContractAuctionBid] = Field(description="The bids.")
    budget: int | float = Field(description="The budget.")
    country: str = Field(description="The UUID of the country this user holds citizenship in.")
    created_at: str = Field(description="The timestamp when this record was created.")
    created_by: str = Field(description="The created by.")
    current_payout: int | float = Field(description="The current payout.")
    current_per_k: int | float = Field(description="The current per k.")
    current_winner: str | None = Field(default=None, description="The current winner.")
    current_winner_user: str | None = Field(default=None, description="The current winner user.")
    duration: int = Field(description="The duration.")
    expires_at: str = Field(description="The expires at.")
    for_country: str = Field(description="The for country.")
    for_country_side: str = Field(description="The for country side.")
    initial_per_k: int | float = Field(description="The initial per k.")
    minimum_damage: int | float = Field(description="The minimum damage.")
    professionals_only: bool = Field(description="The professionals only.")
    round: str = Field(description="The round.")
    round_number: int = Field(description="The round number.")
    status: str = Field(description="The status.")
    updated_at: str = Field(description="The timestamp when this record was last modified.")
