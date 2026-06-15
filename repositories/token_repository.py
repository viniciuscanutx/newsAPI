from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase

class TokenRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.refresh_tokens

    async def save_refresh_token(self, user_id: str, token: str, expires_at: datetime) -> None:
        await self._collection.insert_one({
            "user_id": user_id,
            "token": token,
            "expires_at": expires_at,
        })

    async def find_valid_refresh_token(self, token: str) -> dict | None:
        return await self._collection.find_one({"token": token})

    async def revoke_refresh_token(self, token: str) -> None:
        await self._collection.delete_one({"token": token})