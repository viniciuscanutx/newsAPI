from fastapi import APIRouter, Depends

from dependencies.auth import get_auth_service, get_current_user
from model.auth import (
    EmailRegisteredResponse,
    LoginRequest,
    RegisterUserRequest,
    TokenRefresh,
    TokenResponse,
    ValidateMailRequest,
)
from model.user import InterestsUpdateRequest, PreferencesUpdateRequest, User
from services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/validate", response_model=EmailRegisteredResponse)
async def validate_email(
    request: ValidateMailRequest,
    auth: AuthService = Depends(get_auth_service),
) -> EmailRegisteredResponse:
    is_registered = await auth.validate_email(request.email)
    return EmailRegisteredResponse(is_registered=is_registered)


@router.post("/register", response_model=TokenResponse)
async def register_user(
    request: RegisterUserRequest,
    auth: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth.register_user(request.email, request.password, request.name)


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    auth: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth.login(request.email, request.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: TokenRefresh,
    auth: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    return await auth.refresh(request.refresh_token)


@router.get("/me", response_model=User)
async def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.post("/logout", response_model=None)
async def logout(current_user: User = Depends(get_current_user), auth: AuthService = Depends(get_auth_service)) -> None:
    await auth.logout(current_user.id)
    return None


@router.put("/interests", response_model=User)
async def update_interests(
    request: InterestsUpdateRequest,
    current_user: User = Depends(get_current_user),
    auth: AuthService = Depends(get_auth_service),
) -> User:
    return await auth.update_interests(current_user.id, request)


@router.put("/preferences", response_model=User)
async def update_preferences(
    request: PreferencesUpdateRequest,
    current_user: User = Depends(get_current_user),
    auth: AuthService = Depends(get_auth_service),
) -> User:
    return await auth.update_preferences(current_user.id, request)

