from fastapi import HTTPException, status
from datetime import UTC, datetime

from core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from model.auth import TokenResponse
from model.user import InterestsUpdateRequest, PreferencesUpdateRequest, User, document_to_user
from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, users: UserRepository, tokens: TokenRepository) -> None:
        self._users = users
        self._tokens = tokens

    async def _issue_tokens(self, user_id: str) -> TokenResponse:
        access_token, access_token_expires_in = create_access_token(user_id)
        refresh_token, refresh_token_expires_at = create_refresh_token()
        await self._tokens.save_refresh_token(user_id, refresh_token, refresh_token_expires_at)
        return TokenResponse(
            access_token=access_token,
            expires_in=access_token_expires_in,
            refresh_token=refresh_token,
        )

    async def validate_email(self, email: str) -> bool:
        user = await self._users.find_by_email(email)
        return user is not None

    async def register_user(self, email: str, password: str, name: str) -> TokenResponse:
        existing = await self._users.find_by_email(email)
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado.",
            )

        hashed = hash_password(password)
        document = await self._users.create(
            {"email": email, "name": name, "hashed_password": hashed}
        )

        return await self._issue_tokens(document["_id"])

    async def login(self, email: str, password: str) -> TokenResponse:
        user = await self._users.find_by_email(email)

        if not user or not verify_password(password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos.",
            )
        
        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário desativado.",
            )

        return await self._issue_tokens(str(user["_id"]))

    async def refresh(self, refresh_token: str) -> TokenResponse:
        stored = await self._tokens.find_valid_refresh_token(refresh_token)

        if not stored:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de refresh inválido.",
            )

        expires_at = stored["expires_at"]
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        if expires_at <= datetime.now(UTC):
            await self._tokens.revoke_refresh_token(refresh_token)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de refresh expirado.",
            )

        user = await self._users.find_by_id(stored["user_id"])
        if not user:
            await self._tokens.revoke_refresh_token(refresh_token)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado.",
            )

        await self._tokens.revoke_refresh_token(refresh_token)
        return await self._issue_tokens(stored["user_id"])

    async def update_interests(self, user_id: str, request: InterestsUpdateRequest) -> User:
        document = await self._users.update_interests(
            user_id,
            [category.value for category in request.preferred_categories],
            request.whitelist,
            request.blacklist,
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado.",
            )

        return document_to_user(document)

    async def update_preferences(self, user_id: str, request: PreferencesUpdateRequest) -> User:
        if request.dark_mode is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Informe ao menos uma preferência.",
            )

        document = await self._users.update_preferences(user_id, request.dark_mode)

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado.",
            )

        return document_to_user(document)