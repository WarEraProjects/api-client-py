from __future__ import annotations

from pydantic import Field

from .common import WareraModel


class ArticleStats(WareraModel):
    comments: int | None = Field(default=None, description="The comments.")
    dislikes: int | None = Field(default=None, description="The dislikes.")
    gem_tips: int | None = Field(default=None, description="The gem tips.")
    likes: int | None = Field(default=None, description="The likes.")
    score: int | None = Field(default=None, description="The score.")
    subs: int | None = Field(default=None, description="The subs.")
    tips: int | None = Field(default=None, description="The tips.")
    views: int | None = Field(default=None, description="The views.")


class Article(WareraModel):
    title: str | None = Field(default=None, description="The title.")
    content: str | None = Field(default=None, description="The content.")
    author_id: str | None = Field(default=None, description="The author id.")
    country_id: str | None = Field(default=None, description="The country id.")
    type: str | None = Field(default=None, description="The type.")
    category: str | None = Field(default=None, description="The category.")
    language: str | None = Field(default=None, description="The language.")
    score: int | None = Field(default=None, description="The score.")
    views: int | None = Field(default=None, description="The views.")
    comments: int | None = Field(default=None, description="The comments.")
    image: str | None = Field(default=None, description="The image.")
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    author: str | None = Field(default=None, description="The author.")
    is_deleted: bool | None = Field(default=None, description="The is deleted.")
    is_published: bool | None = Field(default=None, description="The is published.")
    is_public: bool | None = Field(default=None, description="The is public.")
    slug: str | None = Field(default=None, description="The slug.")
    published_at: str | None = Field(default=None, description="The published at.")
    stats: ArticleStats | None = Field(default=None, description="The stats.")
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )


class ArticleLite(WareraModel):
    title: str | None = Field(default=None, description="The title.")
    author_id: str | None = Field(default=None, description="The author id.")
    country_id: str | None = Field(default=None, description="The country id.")
    type: str | None = Field(default=None, description="The type.")
    category: str | None = Field(default=None, description="The category.")
    language: str | None = Field(default=None, description="The language.")
    score: int | None = Field(default=None, description="The score.")
    views: int | None = Field(default=None, description="The views.")
    image: str | None = Field(default=None, description="The image.")
    created_at: str | None = Field(
        default=None, description="The timestamp when this record was created."
    )
    author: str | None = Field(default=None, description="The author.")
    content: str | None = Field(default=None, description="The content.")
    is_deleted: bool | None = Field(default=None, description="The is deleted.")
    is_published: bool | None = Field(default=None, description="The is published.")
    is_public: bool | None = Field(default=None, description="The is public.")
    slug: str | None = Field(default=None, description="The slug.")
    published_at: str | None = Field(default=None, description="The published at.")
    stats: ArticleStats | None = Field(default=None, description="The stats.")
    updated_at: str | None = Field(
        default=None, description="The timestamp when this record was last modified."
    )
