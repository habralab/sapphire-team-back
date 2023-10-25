from autotests.rest.client import BaseRestClient

from .models import HealthResponse


class MessengerRestClient(BaseRestClient):
    async def get_health(self) -> HealthResponse:
        path = "/api/v1beta/rest/health"

        return await self.rest_get(path=path, response_model=HealthResponse)
