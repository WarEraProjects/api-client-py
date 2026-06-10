"""
Shared Pydantic base types used across all models.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

T = TypeVar("T")


def _base_config() -> ConfigDict:
    """
    Standard model config applied to every WarEra model:
      • camelCase aliases (API returns camelCase, Python uses snake_case)
      • extra fields allowed (forward-compatible with schema additions)
      • populate_by_name lets you use either the alias or field name
    """
    return ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="allow",
    )


class ReprMixin:
    """
    Adds a full ``ClassName(field=value, ...)`` repr to plain (non-Pydantic)
    helper classes, including every attribute from ``__slots__`` or ``__dict__``.
    """

    __slots__ = ()

    def __repr__(self) -> str:
        slots: tuple[str, ...] = getattr(self, "__slots__", ())
        names = list(slots) if slots else list(getattr(self, "__dict__", {}))
        fields = ", ".join(f"{n}={getattr(self, n, None)!r}" for n in names)
        return f"{self.__class__.__name__}({fields})"


class WareraModel(BaseModel):
    """
    Base class for all response models.

    Printing any model shows every field and value (Pydantic's default
    ``field=value`` rendering — no custom truncation).
    """

    model_config = _base_config()
    id: str | None = Field(default=None, alias="_id")
    version: int | None = Field(default=None, alias="__v")
    """Mongo document version (`__v`), returned by most entity endpoints."""


class CursorPage(WareraModel, Generic[T]):
    """
    Generic cursor-paginated page returned by all paginated endpoints.

    Usage:
        page: CursorPage[User] = await client.user.get_by_country("7")
        for user in page.items:
            print(user.username)
        if page.has_more:
            next_page = await client.user.get_by_country("7", cursor=page.next_cursor)
    """

    items: list[T]
    next_cursor: str | None = None
    has_more: bool = False

    def __iter__(self):  # type: ignore[no-untyped-def]
        """Make the page iterable directly over its items."""
        return iter(self.items)

    def __len__(self) -> int:
        """Return the number of items on this page."""
        return len(self.items)

    @classmethod
    def from_raw(cls, raw: Any, item_type: type[T]) -> CursorPage[T]:
        """
        Parse a raw API response dict into a typed CursorPage.
        Handles both wrapped `{items, nextCursor}` and plain list responses.
        """
        # Pre-resolve the validator once — all our models are Pydantic BaseModel
        # subclasses so this avoids per-item hasattr + cast overhead.
        _validate = getattr(item_type, "model_validate", None)

        if isinstance(raw, list):
            if _validate is not None:
                items = [_validate(r) for r in raw if isinstance(r, dict)]
            else:
                items = list(raw)
            return cls(items=items, next_cursor=None, has_more=False)

        if isinstance(raw, dict):
            raw_items = raw.get("items", raw.get("data", []))
            if isinstance(raw_items, list):
                if _validate is not None:
                    items = [_validate(r) for r in raw_items if isinstance(r, dict)]
                else:
                    items = list(raw_items)
            else:
                items = []

            next_cursor = raw.get("nextCursor") or raw.get("next_cursor")
            has_more = bool(raw.get("hasMore", raw.get("has_more", bool(next_cursor))))
            return cls(items=items, next_cursor=next_cursor, has_more=has_more)

        return cls(items=[], next_cursor=None, has_more=False)
