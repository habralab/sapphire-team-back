import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreateChat(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    members_ids: list[uuid.UUID]
    is_personal: bool

