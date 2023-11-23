import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.notifications.database.models import Notification
from sapphire.notifications.database.service import NotificationsDatabaseService

from .dependencies import get_path_notification
from .schemas import (
    NotificationFiltersRequest,
    NotificationListResponse,
    NotificationResponse,
    UpdateNotificationRequest,
)


async def get_notifications(
        request: fastapi.Request,
        filters: NotificationFiltersRequest = fastapi.Depends(NotificationFiltersRequest),
        jwt_data: JWTData = fastapi.Depends(is_auth),
        pagination: Pagination = fastapi.Depends(pagination),
) -> NotificationListResponse:
    database_service: NotificationsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        notifications = await database_service.get_notifications(
            page=pagination.page,
            per_page=pagination.per_page,
            session=session,
            is_read=filters.is_read,
            recipient_id=jwt_data.user_id
        )

    notifications = [
        NotificationResponse.model_validate(notification)
        for notification in notifications
    ]

    return NotificationListResponse(
        data=notifications,
        page=pagination.page,
        per_page=pagination.per_page,
    )


async def get_notification(
        notification: Notification = fastapi.Depends(get_path_notification),
) -> NotificationResponse:
    return NotificationResponse.model_validate(notification)


async def update_notification(
        request: fastapi.Request,
        notification: Notification = fastapi.Depends(get_path_notification),
        data: UpdateNotificationRequest = fastapi.Body(embed=False),
) -> NotificationResponse:
    database_service: NotificationsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        await database_service.update_notification(
            session=session,
            notification=notification,
            is_read=data.is_read,
        )

    return NotificationResponse.model_validate(notification)
