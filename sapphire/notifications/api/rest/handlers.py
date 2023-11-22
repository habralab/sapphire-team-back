import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.notifications.api.rest.schemas import (
    Notification,
    NotificationFilters,
    NotificationListModel,
)
from sapphire.notifications.database.service import NotificationsDatabaseService


async def get_notifications(
        request: fastapi.Request,
        filters: NotificationFilters = fastapi.Depends(NotificationFilters),
        jwt_data: JWTData = fastapi.Depends(is_auth),
        pagination: Pagination = fastapi.Depends(pagination),
) -> NotificationListModel:
    database_service: NotificationsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        notifications = await database_service.get_notifications(
            page=pagination.page,
            per_page=pagination.per_page,
            session=session,
            is_read=filters.is_read,
            recipient_id=jwt_data.user_id
        )

    notifications = [Notification.model_validate(notification) for notification in notifications]

    return NotificationListModel(
        data=notifications,
        page=pagination.page,
        per_page=pagination.per_page,
    )
