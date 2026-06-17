from datetime import UTC, datetime

from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

class UserRepository:
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.users
    
    async def find_by_email(self, email: str) -> dict | None:
        return await self._collection.find_one({"email": email.lower()})

    async def find_by_id(self, user_id: str) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None
        return await self._collection.find_one({"_id": ObjectId(user_id)})

    async def create(self, data: dict) -> dict:
        now = datetime.now(UTC)
        document = {
            "email": data["email"].lower(),
            "name": data["name"],
            "hashed_password": data["hashed_password"],
            "preferred_categories": [],
            "whitelist": [],
            "blacklist": [],
            "preferences": {"dark_mode": False},
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }

        result = await self._collection.insert_one(document)
        document["_id"] = str(result.inserted_id)
        return document

    async def update_interests(
        self,
        user_id: str,
        preferred_categories: list[str],
        whitelist: list[str],
        blacklist: list[str],
    ) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None

        return await self._collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "preferred_categories": preferred_categories,
                    "whitelist": whitelist,
                    "blacklist": blacklist,
                    "updated_at": datetime.now(UTC),
                }
            },
            return_document=ReturnDocument.AFTER,
        )

    async def update_preferences(self, user_id: str, dark_mode: bool) -> dict | None:
        if not ObjectId.is_valid(user_id):
            return None

        return await self._collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "preferences.dark_mode": dark_mode,
                    "updated_at": datetime.now(UTC),
                }
            },
            return_document=ReturnDocument.AFTER,
        )
