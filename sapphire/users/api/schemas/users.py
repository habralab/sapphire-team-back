import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr

from sapphire.users.database.models import User


class UserUpdateRequest(BaseModel):
    first_name: str
    last_name: str
    main_specialization_id: uuid.UUID
    secondary_specialization_id: uuid.UUID


class UserResponse(BaseModel):
    id: uuid.UUID
    first_name: str | None
    last_name: str | None
    about: str | None
    main_specialization_id: uuid.UUID | None
    secondary_specialization_id: uuid.UUID | None
    updated_at: datetime
    created_at: datetime

    @classmethod
    def from_db_model(cls, user: User) -> "UserResponse":
        return cls(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            about=user.profile.about,
            main_specialization_id=user.profile.main_specialization_id,
            secondary_specialization_id=user.profile.secondary_specialization_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class UserFullResponse(UserResponse):
    email: EmailStr

    @classmethod
    def from_db_model(cls, user: User) -> "UserFullResponse":
        return cls(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            about=user.profile.about,
            main_specialization_id=user.profile.main_specialization_id,
            secondary_specialization_id=user.profile.secondary_specialization_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
