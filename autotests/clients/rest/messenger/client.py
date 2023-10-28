from autotests.clients.rest.base_client import BaseRestClient

from .models import HealthResponse


class MessengerRestClient(BaseRestClient):
    async def get_health(self) -> HealthResponse:
        path = "/api/rest/health"

        return await self.rest_get(path=path, response_model=HealthResponse)