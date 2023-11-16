import uuid
from typing import Type

from autotests.clients.rest.base_client import BaseRestClient
from autotests.utils import Empty

from .models import (
    ChatListResponse,
    ChatResponse,
    CreateMessageRequest,
    HealthResponse,
    MessageListResponse,
    MessageResponse,
)


class MessengerRestClient(BaseRestClient):
    async def get_health(self) -> HealthResponse:
        path = "/health"

        return await self.rest_get(path=path, response_model=HealthResponse)

    async def get_chats(self, members: set[uuid.UUID] | Type[Empty] = Empty) -> ChatListResponse:
        path = "/api/rest/chats/"
        params = {
            "member": [str(member) for member in members] if isinstance(members, set) else Empty,
        }
        params = {key: value for key, value in params.items() if value is not Empty}

        return await self.rest_get(path=path, params=params, response_model=ChatListResponse)

    async def get_chat(self, chat_id: uuid.UUID) -> ChatResponse:
        path = f"/api/rest/chats/{chat_id}"

        return await self.rest_get(path=path, response_model=ChatResponse)

    async def get_chat_messages(self, chat_id: uuid.UUID) -> MessageListResponse:
        path = f"/api/rest/chats/{chat_id}/messages/"

        return await self.rest_get(path=path, response_model=MessageListResponse)

    async def create_chat_message(self, chat_id: uuid.UUID, text: str) -> MessageResponse:
        path = f"/api/rest/chats/{chat_id}/messages/"
        request = CreateMessageRequest(text=text)

        return await self.rest_post(path=path, data=request, response_model=MessageResponse)
