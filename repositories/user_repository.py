from motor.motor_asyncio import AsyncIOMotorDatabase
from bson.objectid import ObjectId
from datetime import datetime, UTC

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
