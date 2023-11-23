import uuid
from typing import Type


from autotests.clients.rest.base_client import BaseRestClient
from autotests.utils import Empty

from .models import HealthResponse, NotificationListResponse, NotificationResponse


class NotificationsRestClient(BaseRestClient):
    async def get_health(self) -> HealthResponse:
        path = "/health"

        return await self.rest_get(path=path, response_model=HealthResponse)

    async def get_notifications(
            self,
            is_read: bool | Type[Empty] = Empty,
            page: int | Type[Empty] = Empty,
            per_page: int | Type[Empty] = Empty,
    ) -> NotificationListResponse:

        path = "/api/rest/notifications/"

        params = {
            "is_read": is_read,
            "page": page,
            "per_page": per_page,
        }

        params = {key: value for key, value in params.items() if value is not Empty}
        return await self.rest_get(path=path, params=params, response_model=NotificationListResponse)

    async def get_notification(self, notification_id: uuid.UUID) -> NotificationResponse:
        path = f"/api/rest/notifications/{notification_id}"

        return await self.rest_get(path=path, response_model=NotificationResponse)
