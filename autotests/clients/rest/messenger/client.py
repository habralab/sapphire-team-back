from autotests.clients.rest.base_client import BaseRestClient

from .models import ChatListResponse, HealthResponse


class MessengerRestClient(BaseRestClient):
    async def get_health(self) -> HealthResponse:
        path = "/health"

        return await self.rest_get(path=path, response_model=HealthResponse)

    async def get_chats(self) -> ChatListResponse:
        path = "/api/rest/chats/"

        return await self.rest_get(path=path, response_model=ChatListResponse)
