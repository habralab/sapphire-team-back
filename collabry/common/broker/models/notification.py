import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class Notification(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | None = None
    type: str
    recipient_id: uuid.UUID
    data: dict[str, Any]
    created_at: datetime | None = None
    updated_at: datetime | None = None
