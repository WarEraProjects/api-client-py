from __future__ import annotations

import typing
from collections.abc import AsyncIterator

from .._enums import ArticleType
from ..models.article import Article, ArticleLite
from ..models.common import CursorPage
from ._base import BaseResource


class ArticleResource(BaseResource):
    """
    Endpoints:
      • article.getArticleById
      • article.getArticleLiteById
      • article.getArticlesPaginated  (cursor-paginated)
    """

    async def get(self, article_id: str) -> Article:
        """Get a full article by ID (includes content body)."""
        raw = await self._get("article.getArticleById", articleId=article_id)
        return Article.model_validate(raw)

    async def get_lite(self, article_id: str) -> ArticleLite:
        """Get a lightweight article by ID (metadata only, no content body)."""
        raw = await self._get("article.getArticleLiteById", articleId=article_id)
        return ArticleLite.model_validate(raw)

    @typing.overload
    async def get_paginated(
        self,
        type: ArticleType | str,
        *,
        limit: int = 10,
        cursor: str | None = None,
        user_id: str | None = None,
        categories: list[str] | None = None,
        languages: list[str] | None = None,
        positive_score_only: bool | None = None,
        auto_items: typing.Literal[True],
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> AsyncIterator[ArticleLite]: ...

    @typing.overload
    async def get_paginated(
        self,
        type: ArticleType | str,
        *,
        limit: int = 10,
        cursor: str | None = None,
        user_id: str | None = None,
        categories: list[str] | None = None,
        languages: list[str] | None = None,
        positive_score_only: bool | None = None,
        auto_items: typing.Literal[False] = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[ArticleLite]: ...

    async def get_paginated(
        self,
        type: ArticleType | str,
        *,
        limit: int = 10,
        cursor: str | None = None,
        user_id: str | None = None,
        categories: list[str] | None = None,
        languages: list[str] | None = None,
        positive_score_only: bool | None = None,
        auto_items: bool = False,
        max_pages: int | float = float("inf"),
        cursor_end: str | None = None,
    ) -> CursorPage[ArticleLite] | AsyncIterator[ArticleLite]:
        """
        Get articles (cursor-paginated).

        Args:
            type:               Article feed type (daily, weekly, top, my, subscriptions, last).
            user_id:            Filter to articles by a specific author.
            categories:         Filter by category list.
            languages:          Filter by language codes (e.g. ["en", "ro"]).
            positive_score_only: When True, exclude downvoted articles.
            auto_paginate:      If True, returns an AsyncIterator of CursorPages.
            max_pages:          Maximum number of pages to fetch when auto-paginating.
            cursor_end:         Date string. Auto-pagination stops when cursor date is older than this.
        """
        if auto_items:
            from .._pagination import auto_paginate_items

            return auto_paginate_items(
                self.get_paginated,
                max_pages=max_pages,
                cursor_end=cursor_end,
                **{
                    k: v
                    for k, v in locals().items()
                    if k
                    not in (
                        "self",
                        "auto_paginate",
                        "auto_items",
                        "max_pages",
                        "cursor_end",
                        "kwargs",
                    )
                },
            )

        raw = await self._get(
            "article.getArticlesPaginated",
            type=type,
            limit=limit,
            cursor=cursor,
            userId=user_id,
            categories=categories,
            languages=languages,
            positiveScoreOnly=positive_score_only,
        )
        return CursorPage.from_raw(raw, ArticleLite)


    async def collect_all(self, **kwargs: typing.Any) -> list[ArticleLite]:
        """Fetch all items across all pages concurrently using parallel time-slicing."""
        import warnings

        warnings.warn(
            "`collect_all()` is deprecated. Use `get_all()` directly.",
            DeprecationWarning,
            stacklevel=2,
        )
        from .._pagination import parallel_collect_all

        fetch_fn = (
            getattr(self, "get_paginated", None)
            or getattr(self, "get_many", None)
            or getattr(self, "get_all", None)
        )
        if fetch_fn is None:
            raise NotImplementedError("Pagination not supported on this resource")

        return await parallel_collect_all(
            fetch_fn,
            oldest_date=kwargs.pop("oldest_date", None),
            time_slice_days=kwargs.pop("time_slice_days", 0.2),
            concurrency=kwargs.pop("concurrency", 500),
            **kwargs,
        )
