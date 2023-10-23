from autotests.rest.client import BaseRestClient

from .models import HealthResponse


class ProjectsRestClient(BaseRestClient):
    async def get_health(self) -> HealthResponse:
        path = "/api/v1beta/rest/health"

        response = await self.get(url=path)

        return HealthResponse.model_validate(response.json())
