from __future__ import annotations

from pydantic import Field

from .common import WareraModel


class GovernmentDates(WareraModel):
    announcement_created_ats: list[str] | None = Field(
        default=None, description="The announcement created ats."
    )


class Government(WareraModel):
    dates: GovernmentDates | None = Field(default=None, description="The dates.")
    country: str | None = Field(
        default=None, description="The UUID of the country this user holds citizenship in."
    )
    country_id: str | None = Field(default=None, description="The country id.")
    president: str | None = Field(
        default=None, description="The UUID of the user currently holding the office of President."
    )
    vice_president: str | None = Field(default=None, description="The vice president.")
    min_of_defense: str | None = Field(default=None, description="The min of defense.")
    min_of_economy: str | None = Field(default=None, description="The min of economy.")
    min_of_foreign_affairs: str | None = Field(
        default=None, description="The min of foreign affairs."
    )
    # Use default_factory so each Government instance gets its own list.
    # A bare `= []` class-level default would be shared across all instances,
    # which is a classic mutable-default bug even though Pydantic v2 copies it
    # internally — it's still inconsistent with every other list field here
    # and signals the wrong intent to readers.
    congress_members: list[str] = Field(default_factory=list)

    def has_president(self) -> bool:
        return self.president is not None
