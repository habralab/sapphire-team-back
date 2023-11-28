import uuid

from pydantic import BaseModel, EmailStr


class GetUserRequest(BaseModel):
    id: uuid.UUID


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str | None
    last_name: str | None
    is_activated: bool
    
    about: str | None
    main_specialization_id: uuid.UUID | None
    secondary_specialization_id: uuid.UUID | None
