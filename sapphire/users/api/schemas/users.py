import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserUpdateRequest(BaseModel):
    first_name: str
    last_name: str


class UserFullResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    updated_at: datetime
    created_at: datetime
