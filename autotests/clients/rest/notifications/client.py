from autotests.clients.rest.base_client import BaseRestClient

from .models import HealthResponse


class NotificationsRestClient(BaseRestClient):
    async def get_health(self) -> HealthResponse:
        path = "/health"

        return await self.rest_get(path=path, response_model=HealthResponse)
