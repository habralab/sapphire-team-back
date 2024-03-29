import uuid
from typing import Literal

from pydantic import AwareDatetime, BaseModel, EmailStr, constr

Password = constr(pattern=r"^[\w\(\)\[\]\{}\^\$\+\*@#%!&]{8,}$")


class HealthResponse(BaseModel):
    name: Literal["Users"]
    version: constr(pattern=r"^\d+\.\d+\.\d+$")


class JWTData(BaseModel):
    user_id: uuid.UUID
    is_activated: bool


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr | None
    telegram: str | None
    first_name: str | None
    last_name: str | None
    is_activated: bool
    has_avatar: bool
    about: str | None
    main_specialization_id: uuid.UUID | None
    secondary_specialization_id: uuid.UUID | None
    created_at: AwareDatetime
    updated_at: AwareDatetime


class UserUpdateRequest(BaseModel):
    first_name: str
    last_name: str
    about: str | None
    telegram: str | None
    main_specialization_id: uuid.UUID | None
    secondary_specialization_id: uuid.UUID | None


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
    email: EmailStr
    code: str
    new_password: Password
