import uuid
from datetime import datetime

from pydantic import BaseModel


class UserUpdateRequest(BaseModel):
    user_id: uuid.UUID
    first_name: str
    last_name: str


class UserUpdateResponce(BaseModel):
    user_id: uuid.UUID
    first_name: str
    last_name: str
    update_at: datetime
