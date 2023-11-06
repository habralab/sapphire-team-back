import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from sapphire.users.database.models import Skill, User


class UserUpdateRequest(BaseModel):
    first_name: str | None
    last_name: str | None
    about: str | None
    main_specialization_id: uuid.UUID | None
    secondary_specialization_id: uuid.UUID | None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: EmailStr | None
    first_name: str | None
    last_name: str | None
    about: str | None
    main_specialization_id: uuid.UUID | None
    secondary_specialization_id: uuid.UUID | None
    updated_at: datetime
    created_at: datetime

    @classmethod
    def from_db_model(cls, user: User, with_email: bool = True) -> "UserResponse":
        return cls(
            id=user.id,
            email=user.email if with_email else None,
            first_name=user.first_name,
            last_name=user.last_name,
            about=user.profile.about,
            main_specialization_id=user.profile.main_specialization_id,
            secondary_specialization_id=user.profile.secondary_specialization_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class UserSkillResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    skill_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserSkillsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_skills: list[UserSkillResponse]
