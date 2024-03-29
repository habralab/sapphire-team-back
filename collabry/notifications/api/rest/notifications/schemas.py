import uuid
from typing import Any, Literal, Type

from pydantic import AwareDatetime, BaseModel, ConfigDict

from collabry.common.api.schemas.paginated import PaginatedResponse
from collabry.common.utils.empty import Empty


class UpdateNotificationRequest(BaseModel):
    is_read: Literal[True]


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: str
    recipient_id: uuid.UUID
    data: dict[str, Any]
    is_read: bool
    created_at: AwareDatetime
    updated_at: AwareDatetime


class NotificationFiltersRequest(BaseModel):
    is_read: bool | Type[Empty] = Empty


class NotificationListResponse(PaginatedResponse):
    data: list[NotificationResponse]
