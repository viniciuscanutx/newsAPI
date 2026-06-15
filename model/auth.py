from pydantic import BaseModel, EmailStr, Field

class ValidateMailRequest(BaseModel):
    email: EmailStr

class EmailRegisteredResponse(BaseModel):
    is_registered: bool

class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    name: str = Field(min_length=3, max_length=100)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenRefresh(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: str | None = None
