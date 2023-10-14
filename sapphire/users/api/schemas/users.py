import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserUpdateRequest(BaseModel):
    first_name: str
    last_name: str


class UserResponse(BaseModel):
    id: uuid.UUID
    first_name: str | None
    last_name: str | None
    about: str | None
    main_specialization_id: uuid.UUID | None
    secondary_specialization_id: uuid.UUID | None
    updated_at: datetime
    created_at: datetime


class UserFullResponse(UserResponse):
    email: EmailStr
