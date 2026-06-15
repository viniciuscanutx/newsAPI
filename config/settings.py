from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    mongodb_uri: str = Field(default=os.getenv("MONGODB_URI"))
    mongodb_db: str = Field(default=os.getenv("MONGODB_DB"))
    jwt_secret: str = Field(default=os.getenv("JWT_SECRET"))
    jwt_algorithm: str = Field(default=os.getenv("JWT_ALGORITHM"))
    access_token_expire_minutes: int = Field(default=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    refresh_token_expire_days: int = Field(default=os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    cors_origins: str = Field(default=os.getenv("CORS_ORIGINS"))
    news_api_key: str = Field(default=os.getenv("NEWS_API_KEY"))

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
