import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Chat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chat_id: uuid.UUID
    name: Optional[str]
    type: str
    is_personal: Optional[bool]
