import uuid
from datetime import datetime
from typing import Type

from pydantic import BaseModel, ConfigDict

from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.common.utils.empty import Empty
from sapphire.messenger.database.models import Chat


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    chat_id: uuid.UUID
    user_id: uuid.UUID
    text: str
    created_at: datetime
    updated_at: datetime


class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_personal: bool
    members: list[uuid.UUID]
    last_message: MessageResponse | None
    created_at: datetime

    @classmethod
    def from_db_model(cls, chat: Chat) -> "ChatResponse":
        return cls(
            id=chat.id,
            is_personal=chat.is_personal,
            members=[member.user_id for member in chat.members],
            last_message=(
                MessageResponse.model_validate(chat.last_message)
                if chat.last_message else
                None
            ),
            created_at=chat.created_at,
        )


class ChatListFiltersRequest(BaseModel):
    member: set[uuid.UUID] | Type[Empty] = Empty


class ChatListResponse(PaginatedResponse):
    data: list[ChatResponse]
