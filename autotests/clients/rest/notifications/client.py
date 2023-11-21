import io
import uuid
from datetime import datetime
from typing import Type, Any

from sqlalchemy.ext.asyncio import AsyncSession

from autotests.clients.rest.base_client import BaseRestClient
from autotests.clients.rest.exceptions import ResponseException
from autotests.clients.rest.notifications.models import NotificationModel, NotificationListResponse
from autotests.utils import Empty

from .models import HealthResponse


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

        path = "/api/rest/notifications"

        params = {
            "is_read": is_read,
            "page": page,
            "per_page": per_page,
        }

        params = {key: value for key, value in params.items() if value is not Empty}
        return await self.rest_get(path=path, params=params, response_model=NotificationListResponse)
