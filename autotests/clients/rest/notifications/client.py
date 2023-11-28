import uuid
from typing import Literal, Type

from autotests.clients.rest.base_client import BaseRestClient
from autotests.clients.rest.exceptions import ResponseException
from autotests.utils import Empty

from .models import (
    HealthResponse,
    NotificationListResponse,
    NotificationResponse,
    UpdateNotificationRequest,
)


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

    async def get_notifications_count(self, is_read: bool | Type[Empty] = Empty) -> int:
        path = "/api/rest/notifications/count"

        params = {"is_read": is_read}
        params = {key: value for key, value in params.items() if value is not Empty}

        response = await self.get(url=path)
        if response.status_code // 100 != 2:
            raise ResponseException(status_code=response.status_code, body=response.content)

        return response.json()

    async def get_notification(self, notification_id: uuid.UUID) -> NotificationResponse:
        path = f"/api/rest/notifications/{notification_id}"

        return await self.rest_get(path=path, response_model=NotificationResponse)

    async def update_notification(
            self,
            notification_id: uuid.UUID,
            is_read: Literal[True],
    ) -> NotificationResponse:
        path = f"/api/rest/notifications/{notification_id}"

        request = UpdateNotificationRequest(is_read=is_read)

        return await self.rest_post(path=path, data=request, response_model=NotificationResponse)
