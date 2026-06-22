from fastapi import APIRouter, Depends

from dependencies.auth import get_current_user
from dependencies.news import get_news_service
from model.enums import FeedCategory
from model.news import IngestNewsResponse
from model.user import User
from services.news_service import NewsService

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/ingest-news", response_model=IngestNewsResponse)
async def ingest_news(
    category: FeedCategory | None = None,
    current_user: User = Depends(get_current_user),
    news: NewsService = Depends(get_news_service),
) -> IngestNewsResponse:
    return await news.ingest_from_newsapi(category)
