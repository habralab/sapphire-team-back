from autotests.rest.client import BaseRestClient

from .models import HealthResponse


class NotificationsRestClient(BaseRestClient):
    def get_health(self) -> HealthResponse:
        path = "/api/v1beta/rest/health"

        response = self.get(path=path)

        return HealthResponse.model_validate(response.json())
