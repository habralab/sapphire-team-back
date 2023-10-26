import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class Messegner(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    senders_id: Optional[uuid.UUID]
    owner_id: Optional[uuid.UUID]
    project_id = Optional[uuid.UUID]
    type: str
    created_at: datetime | None
