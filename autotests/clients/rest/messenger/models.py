import uuid
from typing import Literal

from pydantic import AwareDatetime, BaseModel, constr

from autotests.clients.rest.models import PaginatedResponse


class HealthResponse(BaseModel):
    name: Literal["Messenger"]
    version: constr(pattern=r"^\d+\.\d+\.\d+$")


class MessageResponse(BaseModel):
    id: uuid.UUID
    chat_id: uuid.UUID
    user_id: uuid.UUID
    text: str
    created_at: AwareDatetime
    updated_at: AwareDatetime


class ChatResponse(BaseModel):
    id: uuid.UUID
    is_personal: bool
    members: list[uuid.UUID]
    last_message: MessageResponse | None
    created_at: AwareDatetime


class ChatListResponse(PaginatedResponse):
    data: list[ChatResponse]


class MessageListResponse(PaginatedResponse):
    data: list[MessageResponse]


class CreateMessageRequest(BaseModel):
    text: constr(min_length=1, strip_whitespace=True)
