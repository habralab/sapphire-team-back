import uuid
from datetime import datetime
from typing import Any, Type

from pydantic import BaseModel, ConfigDict

from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.common.utils.empty import Empty


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: str
    recipient_id: uuid.UUID
    data: dict[str, Any]
    is_read: bool
    created_at: datetime
    updated_at: datetime


class NotificationFiltersRequest(BaseModel):
    is_read: bool | Type[Empty] = Empty


class NotificationListResponse(PaginatedResponse):
    data: list[NotificationResponse]
