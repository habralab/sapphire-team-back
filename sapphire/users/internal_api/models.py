import uuid

from pydantic import BaseModel, EmailStr


class GetUserRequest(BaseModel):
    id: uuid.UUID


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_activated: bool = False

    about: str | None = None
    main_specialization_id: uuid.UUID | None = None
    secondary_specialization_id: uuid.UUID | None = None
