from __future__ import annotations

from .common import WareraModel


class ArticleStats(WareraModel):
    comments: int | None = None
    dislikes: int | None = None
    gem_tips: int | None = None
    likes: int | None = None
    score: int | None = None
    subs: int | None = None
    tips: int | None = None
    views: int | None = None


class Article(WareraModel):
    title: str | None = None
    content: str | None = None
    author_id: str | None = None
    country_id: str | None = None
    type: str | None = None
    category: str | None = None
    language: str | None = None
    score: int | None = None
    views: int | None = None
    comments: int | None = None
    image: str | None = None
    created_at: str | None = None
    author: str | None = None
    is_deleted: bool | None = None
    is_published: bool | None = None
    is_public: bool | None = None
    slug: str | None = None
    published_at: str | None = None
    stats: ArticleStats | None = None
    updated_at: str | None = None


class ArticleLite(WareraModel):
    title: str | None = None
    author_id: str | None = None
    country_id: str | None = None
    type: str | None = None
    category: str | None = None
    language: str | None = None
    score: int | None = None
    views: int | None = None
    image: str | None = None
    created_at: str | None = None
    author: str | None = None
    content: str | None = None
    is_deleted: bool | None = None
    is_published: bool | None = None
    is_public: bool | None = None
    slug: str | None = None
    published_at: str | None = None
    stats: ArticleStats | None = None
    updated_at: str | None = None
