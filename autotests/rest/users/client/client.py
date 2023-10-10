from autotests.rest.client import BaseRestClient

from .models import HealthResponse


class UsersRestClient(BaseRestClient):
    def get_health(self) -> HealthResponse:
        path = "/api/v1beta/health"

        response = self.get(path=path)

        return HealthResponse.model_validate(response.json())
