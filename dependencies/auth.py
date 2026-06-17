import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.security import decode_access_token
from database.database import get_database
from model.user import User, document_to_user
from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository
from services.auth_service import AuthService

security = HTTPBearer()


async def get_auth_service() -> AuthService:
    db = get_database()
    return AuthService(UserRepository(db), TokenRepository(db))


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        )

    document = await UserRepository(get_database()).find_by_id(user_id)
    if not document or not document.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado ou inativo.",
        )

    return document_to_user(document)
