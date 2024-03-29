import uuid

import fastapi

from collabry.common.api.exceptions import HTTPForbidden, HTTPNotFound
from collabry.common.jwt.dependencies.rest import is_auth
from collabry.common.jwt.models import JWTData
from collabry.database.models import Notification
from collabry.notifications import database


async def get_path_notification(
        request: fastapi.Request,
        jwt_data: JWTData = fastapi.Depends(is_auth),
        notification_id: uuid.UUID = fastapi.Path(),
) -> Notification:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        notification = await database_service.get_notification(
            session=session,
            notification_id=notification_id,
        )

    if notification is None:
        raise HTTPNotFound()
    if notification.recipient_id != jwt_data.user_id:
        raise HTTPForbidden()

    return notification
