import uuid
from typing import Any, Literal

from pydantic import AwareDatetime, BaseModel, constr

from autotests.clients.rest.models import PaginatedResponse


class HealthResponse(BaseModel):
    name: Literal["Notifications"]
    version: constr(pattern=r"^\d+\.\d+\.\d+$")


class UpdateNotificationRequest(BaseModel):
    is_read: Literal[True]


class NotificationResponse(BaseModel):
    id: uuid.UUID
    type: str
    recipient_id: uuid.UUID
    data: dict[str, Any]
    is_read: bool
    created_at: AwareDatetime
    updated_at: AwareDatetime


class NotificationListResponse(PaginatedResponse):
    data: list[NotificationResponse]
