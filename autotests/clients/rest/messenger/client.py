import uuid
from typing import Type

from autotests.clients.rest.base_client import BaseRestClient
from autotests.utils import Empty

from .models import ChatListResponse, ChatResponse, HealthResponse


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
