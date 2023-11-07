import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, NaiveDatetime

from sapphire.users.database.models import User, UserSkill


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
    updated_at: NaiveDatetime
    created_at: NaiveDatetime

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


class UserSkillsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid
    skills: list[UserSkill]
