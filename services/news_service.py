from datetime import UTC, datetime

import httpx

from config.settings import settings
from model.enums import FeedCategory
from model.news import IngestNewsResponse, NewsDetailRead, NewsItemRead, NewsListResponse
from model.user import User
from repositories.news_repository import NewsRepository

NEWS_API_BASE = "https://newsdata.io/api/1"

NEWS_DATA_TO_OWN: dict[str, str] = {
    "technology": "tech",
    "business": "negocios",
    "entertainment": "cultura",
    "sports": "esportes",
    "politics": "politica",
    "world": "internacional",
    "science": "ciencia",
    "health": "saude",
    "education": "educacao",
    "lifestyle": "relacionamento",
    "food": "gastronomia",
    "automotive": "automotivo",
    "top": "internacional",
    "environment": "ciencia",
    "tourism": "viagem",
}


class NewsService:

    def __init__(self, repository: NewsRepository) -> None:
        self._repo = repository

    async def ingest_from_newsapi(self, category: FeedCategory | None = None) -> IngestNewsResponse:
        inserted = 0
        updated = 0
        skipped = 0

        async with httpx.AsyncClient() as client:
            page_token = None
            pages_fetched = 0
            max_pages = 10

            while pages_fetched < max_pages:
                params: dict = {
                    "apikey": settings.news_api_key,
                    "country": "br",
                    "language": "pt",
                }
                if page_token:
                    params["page"] = page_token

                response = await client.get(f"{NEWS_API_BASE}/latest", params=params)

                if response.status_code != 200:
                    break

                data = response.json()
                raw = data.get("results", [])

                if isinstance(raw, dict):
                    break

                if not raw:
                    break

                for article in raw:
                    if not article.get("title") or not article.get("link"):
                        skipped += 1
                        continue

                    api_cat = (article.get("category") or ["world"])[0]
                    own_cat = NEWS_DATA_TO_OWN.get(api_cat, "internacional")

                    if category and own_cat != category.value:
                        skipped += 1
                        continue

                    news_doc = {
                        "title": article["title"],
                        "summary": article.get("description") or "",
                        "content": article.get("content") or article.get("description") or "",
                        "category": own_cat,
                        "source_url": article["link"],
                        "source_name": article.get("source_name"),
                        "image_url": article.get("image_url"),
                        "author": (article.get("creator") or [None])[0],
                        "published_at": self._parse_date(article.get("pubDate")),
                    }

                    existing = await self._repo.find_by_source_url(article["link"])
                    if existing:
                        updated += 1
                    else:
                        inserted += 1

                    await self._repo.upsert(news_doc)

                page_token = data.get("nextPage")
                pages_fetched += 1

                if not page_token:
                    break

        return IngestNewsResponse(
            inserted=inserted,
            updated=updated,
            skipped=skipped,
        )

    async def get_daily_feed(
        self, user: User, page: int = 1, limit: int = 10, categories: list[str] | None = None
    ) -> NewsListResponse:
        if categories is None:
            categories = [c.value for c in user.preferred_categories]
        items, total = await self._repo.find_daily(
            categories=categories,
            whitelist=user.whitelist,
            blacklist=user.blacklist,
            page=page,
            limit=limit,
        )

        return NewsListResponse(
            items=[self._to_item_read(item) for item in items],
            total=total,
            page=page,
            limit=limit,
        )

    async def get_by_id(self, news_id: str) -> NewsDetailRead | None:
        doc = await self._repo.find_by_id(news_id)
        if not doc:
            return None
        return self._to_detail_read(doc)

    def _to_item_read(self, doc: dict) -> NewsItemRead:
        return NewsItemRead(
            id=str(doc["_id"]),
            title=doc["title"],
            summary=doc.get("summary") or "",
            content=doc.get("content") or "",
            category=doc["category"],
            image_url=doc.get("image_url"),
        )

    def _to_detail_read(self, doc: dict) -> NewsDetailRead:
        return NewsDetailRead(
            id=str(doc["_id"]),
            title=doc["title"],
            summary=doc.get("summary") or "",
            content=doc.get("content") or "",
            category=doc["category"],
            image_url=doc.get("image_url"),
            source_name=doc.get("source_name"),
            source_url=doc.get("source_url"),
            published_at=doc.get("published_at"),
        )

    @staticmethod
    def _parse_date(date_str: str | None) -> datetime | None:
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return None
