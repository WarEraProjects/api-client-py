from __future__ import annotations

from pydantic import Field

from .common import WareraModel


class ItemPrice(WareraModel):
    item_code: str | None = Field(default=None, description="The item code.")
    price: float | None = Field(default=None, description="The price.")
    quantity: int | None = Field(default=None, description="The quantity.")
    country_id: str | None = Field(default=None, description="The country id.")
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )


class TradingOrder(WareraModel):
    item_code: str | None = Field(default=None, description="The item code.")
    price: float | None = Field(default=None, description="The price.")
    quantity: int | None = Field(default=None, description="The quantity.")
    order_type: str | None = Field(default=None, description="The order type.")  # "buy" | "sell"
    country: str | None = Field(
        default=None, description="The UUID of the country this user holds citizenship in."
    )
    country_id: str | None = Field(default=None, description="The country id.")
    user_id: str | None = Field(default=None, description="The user id.")
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    expires_at: str | None = Field(default=None, description="The expires at.")
    offer_at: str | None = Field(default=None, description="The offer at.")
    type: str | None = Field(default=None, description="The type.")
    user: str | None = Field(default=None, description="The user.")


class ItemOffer(WareraModel):
    item_code: str | None = Field(default=None, description="The item code.")
    price: float | None = Field(default=None, description="The price.")
    quantity: int | None = Field(default=None, description="The quantity.")
    seller_id: str | None = Field(default=None, description="The seller id.")
    country_id: str | None = Field(default=None, description="The country id.")
    region_id: str | None = Field(default=None, description="The region id.")
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    offer_at: str | None = Field(default=None, description="The offer at.")
    type: str | None = Field(default=None, description="The type.")
    user: str | None = Field(default=None, description="The user.")
