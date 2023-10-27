import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Chat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    requester_id: uuid.UUID
    recipient_id: uuid.UUID
    type: str
    is_personal: bool
