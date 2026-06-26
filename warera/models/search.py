from __future__ import annotations

from pydantic import Field

from .common import WareraModel


class SearchResult(WareraModel):
    # Override the _id alias inherited from WareraModel: search results use a
    # plain 'id' field, not a MongoDB '_id'. Without this override the alias
    # would cause a plain 'id' key in a raw dict to be missed when using
    # model_validate() with an unaliased dict.
    type: str | None = Field(
        default=None, description="The type. Can be user, country, company, mu, or article."
    )


class SearchResults(WareraModel):
    results: list[SearchResult] = Field(default_factory=list)
    total: int | None = Field(default=None, description="The total.")
