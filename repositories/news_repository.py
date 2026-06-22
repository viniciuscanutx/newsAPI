from datetime import UTC, datetime

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument


class NewsRepository:

    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.news

    async def upsert(self, data: dict) -> str:
        source_url = data.get("source_url")
        existing = await self._collection.find_one({"source_url": source_url})

        if existing:
            await self._collection.update_one(
                {"_id": existing["_id"]},
                {"$set": {**data, "updated_at": datetime.now(UTC)}},
            )
            return str(existing["_id"])

        data["ingested_at"] = datetime.now(UTC)
        result = await self._collection.insert_one(data)
        return str(result.inserted_id)

    async def find_by_source_url(self, source_url: str) -> dict | None:
        return await self._collection.find_one({"source_url": source_url})

    async def find_by_id(self, news_id: str) -> dict | None:
        if not ObjectId.is_valid(news_id):
            return None
        return await self._collection.find_one({"_id": ObjectId(news_id)})

    async def find_daily(
        self,
        categories: list[str],
        whitelist: list[str],
        blacklist: list[str],
        page: int = 1,
        limit: int = 10,
    ) -> tuple[list[dict], int]:
        query: dict = {}

        if categories:
            query["category"] = {"$in": categories}

        if whitelist:
            query["source_name"] = {"$in": whitelist}

        if blacklist:
            query["source_name"] = {"$nin": blacklist}

        total = await self._collection.count_documents(query)
        skip = (page - 1) * limit
        cursor = (
            self._collection.find(query)
            .sort("published_at", -1)
            .skip(skip)
            .limit(limit)
        )
        items = await cursor.to_list(length=limit)
        return items, total

    async def count_all(self) -> int:
        return await self._collection.count_documents({})
