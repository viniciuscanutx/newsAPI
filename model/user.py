from pydantic import BaseModel, Field

from model.enums import FeedCategory

class UserFeedSettings(BaseModel):
    preferred_categories: list[FeedCategory] = Field(default_factory=list)
    whitelist: list[str] = Field(default_factory=list)
    blacklist: list[str] = Field(default_factory=list)


class UserPreferences(BaseModel):
    dark_mode: bool = False


class InterestsUpdateRequest(UserFeedSettings):
    pass


class PreferencesUpdateRequest(BaseModel):
    dark_mode: bool | None = None


class User(UserFeedSettings):
    id: str
    email: str
    name: str
    is_active: bool
    preferences: UserPreferences = Field(default_factory=UserPreferences)


class UserRead(UserFeedSettings):
    id: str
    name: str
    is_active: bool
    preferences: UserPreferences = Field(default_factory=UserPreferences)
