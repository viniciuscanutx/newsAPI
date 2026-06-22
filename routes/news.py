from fastapi import APIRouter, Depends, Query

from dependencies.auth import get_current_user
from dependencies.news import get_news_service
from model.enums import FeedCategory
from model.news import IngestNewsResponse, NewsDetailRead, NewsListResponse
from model.user import User
from services.news_service import NewsService

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/daily", response_model=NewsListResponse)
async def daily_feed(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    interest_ids: str | None = Query(None, alias="interestIds"),
    current_user: User = Depends(get_current_user),
    news: NewsService = Depends(get_news_service),
) -> NewsListResponse:
    categories = None
    if interest_ids:
        categories = [c.strip() for c in interest_ids.split(",") if c.strip()]
    return await news.get_daily_feed(current_user, page=page, limit=limit, categories=categories)


@router.get("/{news_id}", response_model=NewsDetailRead)
async def news_detail(
    news_id: str,
    current_user: User = Depends(get_current_user),
    news: NewsService = Depends(get_news_service),
) -> NewsDetailRead:
    result = await news.get_by_id(news_id)
    if not result:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notícia não encontrada.",
        )
    return result
