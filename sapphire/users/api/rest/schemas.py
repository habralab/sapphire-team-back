import uuid

from pydantic import AwareDatetime, BaseModel, ConfigDict, EmailStr

from sapphire.database.models import User


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
    updated_at: AwareDatetime
    created_at: AwareDatetime

    @classmethod
    def from_db_model(cls, user: User, with_email: bool = True) -> "UserResponse":
        return cls(
            id=user.id,
            email=user.email if with_email else None,
            telegram=user.telegram,
            first_name=user.first_name,
            last_name=user.last_name,
            is_activated=user.is_activated,
            has_avatar=user.has_avatar,
            about=user.profile.about,
            main_specialization_id=user.profile.main_specialization_id,
            secondary_specialization_id=user.profile.secondary_specialization_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
