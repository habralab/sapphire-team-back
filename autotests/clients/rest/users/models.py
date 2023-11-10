import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, constr


class HealthResponse(BaseModel):
    name: Literal["Users"]
    version: constr(pattern=r"^\d+\.\d+\.\d+$")


class JWTData(BaseModel):
    user_id: uuid.UUID
    is_activated: bool


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr | None
    first_name: str | None
    last_name: str | None
    is_activated: bool
    about: str | None
    main_specialization_id: uuid.UUID | None
    secondary_specialization_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class UserUpdateRequest(BaseModel):
    first_name: str | None
    last_name: str | None
    about: str | None
    main_specialization_id: uuid.UUID | None
    secondary_specialization_id: uuid.UUID | None
