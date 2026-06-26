from __future__ import annotations

from pydantic import Field

from .common import WareraModel
from .inventory import Equipment


class Transaction(WareraModel):
    transaction_type: str | None = Field(default=None, description="The transaction type.")
    money: float | None = Field(default=None, description="The money.")
    quantity: int | None = Field(default=None, description="The quantity.")
    seller_id: str | None = Field(default=None, description="The seller id.")
    buyer_id: str | None = Field(default=None, description="The buyer id.")
    item_code: str | None = Field(default=None, description="The item code.")
    # Full item object on itemMarket transactions
    item: Equipment | None = Field(default=None, description="The item.")
    offer_created_at: str | None = Field(default=None, description="The offer created at.")
    # Present on donation / transfer transaction types
    user_id: str | None = Field(default=None, description="The user id.")
    mu_id: str | None = Field(default=None, description="The mu id.")
    country_id: str | None = Field(default=None, description="The country id.")
    party_id: str | None = Field(default=None, description="The party id.")
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )
