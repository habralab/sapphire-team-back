import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.notifications import database
from sapphire.notifications.database.models import Notification

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
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        notifications = await database_service.get_notifications(
            page=pagination.page,
            per_page=pagination.per_page,
            session=session,
            is_read=filters.is_read,
            recipient_id=jwt_data.user_id,
        )
        total_notifications = await database_service.get_notifications_count(
            session=session,
            is_read=filters.is_read,
            recipient_id=jwt_data.user_id,
        )

    total_pages = -(total_notifications // -pagination.per_page)
    notifications = [
        NotificationResponse.model_validate(notification)
        for notification in notifications
    ]

    return NotificationListResponse(
        data=notifications,
        page=pagination.page,
        per_page=pagination.per_page,
        total_items=total_notifications,
        total_pages=total_pages,
    )


async def get_notifications_count(
        request: fastapi.Request,
        filters: NotificationFiltersRequest = fastapi.Depends(NotificationFiltersRequest),
        jwt_data: JWTData = fastapi.Depends(is_auth),
) -> int:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        total_notifications = await database_service.get_notifications_count(
            session=session,
            is_read=filters.is_read,
            recipient_id=jwt_data.user_id,
        )

    return total_notifications


async def get_notification(
        notification: Notification = fastapi.Depends(get_path_notification),
) -> NotificationResponse:
    return NotificationResponse.model_validate(notification)


async def update_notification(
        request: fastapi.Request,
        notification: Notification = fastapi.Depends(get_path_notification),
        data: UpdateNotificationRequest = fastapi.Body(embed=False),
) -> NotificationResponse:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        await database_service.update_notification(
            session=session,
            notification=notification,
            is_read=data.is_read,
        )

    return NotificationResponse.model_validate(notification)
