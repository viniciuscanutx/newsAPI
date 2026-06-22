from database.database import get_database
from repositories.news_repository import NewsRepository
from services.news_service import NewsService


async def get_news_service() -> NewsService:
    db = get_database()
    return NewsService(NewsRepository(db))
