from __future__ import annotations

from .common import WareraModel
from .inventory import Equipment


class Transaction(WareraModel):
    transaction_type: str | None = None
    money: float | None = None
    quantity: int | None = None
    seller_id: str | None = None
    buyer_id: str | None = None
    item_code: str | None = None
    # Full item object on itemMarket transactions
    item: Equipment | None = None
    offer_created_at: str | None = None
    # Present on donation / transfer transaction types
    user_id: str | None = None
    mu_id: str | None = None
    country_id: str | None = None
    party_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
