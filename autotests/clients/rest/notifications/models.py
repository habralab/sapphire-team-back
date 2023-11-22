import uuid
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, constr

from autotests.clients.rest.models import PaginatedResponse


class HealthResponse(BaseModel):
    name: Literal["Notifications"]
    version: constr(pattern=r"^\d+\.\d+\.\d+$")


class NotificationModel(BaseModel):
    id: uuid.UUID
    type: str
    recipient_id: uuid.UUID
    data: dict[str, Any]
    is_read: bool
    created_at: datetime
    updated_at: datetime


class NotificationListResponse(PaginatedResponse):
    data: list[NotificationModel]
