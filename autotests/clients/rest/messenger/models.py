import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, constr

from autotests.clients.rest.models import PaginatedResponse


class HealthResponse(BaseModel):
    name: Literal["Messenger"]
    version: constr(pattern=r"^\d+\.\d+\.\d+$")


class MessageResponse(BaseModel):
    id: uuid.UUID
    chat_id: uuid.UUID
    text: str
    created_at: datetime
    updated_at: datetime


class ChatResponse(BaseModel):
    id: uuid.UUID
    is_personal: bool
    members: list[uuid.UUID]
    last_message: MessageResponse | None
    created_at: datetime


class ChatListResponse(PaginatedResponse):
    data: list[ChatResponse]
