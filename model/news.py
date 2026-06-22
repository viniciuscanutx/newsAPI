from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from model.enums import FeedCategory


class News(BaseModel):
    id: str | None = None
    kind: Literal["news"] = "news"
    title: str
    summary: str
    content: str
    category: FeedCategory
    source_url: str
    source_name: str | None = None
    image_url: str | None = None
    author: str | None = None
    published_at: datetime | None = None
    ingested_at: datetime | None = None


class NewsItemRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True, serialize_by_alias=True)

    id: str
    title: str
    summary: str = ""
    content: str = ""
    category: FeedCategory
    image_url: str | None = Field(default=None, alias="imageUrl")


class NewsListResponse(BaseModel):
    items: list[NewsItemRead]
    total: int
    page: int
    limit: int


class NewsDetailRead(NewsItemRead):
    source_name: str | None = Field(default=None, alias="sourceName")
    source_url: str | None = Field(default=None, alias="sourceUrl")
    published_at: datetime | None = Field(default=None, alias="publishedAt")


class IngestNewsResponse(BaseModel):
    inserted: int
    updated: int
    skipped: int
    message: str = Field(default="Ingestão de notícias concluída com sucesso!")
