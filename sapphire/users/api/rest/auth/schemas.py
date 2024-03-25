from pydantic import BaseModel, EmailStr

from sapphire.common.types import Password
from sapphire.users.api.rest.schemas import UserResponse


class AuthorizeRequest(BaseModel):
    email: EmailStr
    password: Password


class AuthorizeResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class ChangePasswordRequest(BaseModel):
    code: str
    email: EmailStr
    new_password: Password
