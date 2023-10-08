import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Notification(BaseModel):
    id: uuid.UUID | None
    type: str
    recipient_id: uuid.UUID
    data: dict[str, Any]

    created_at: datetime | None
    updated_at: datetime | None
