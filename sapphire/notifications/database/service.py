import pathlib
import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.notifications.settings import NotificationsSettings

from .models import Notification


class NotificationsDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    def create_notification(
            self,
            session: AsyncSession,
            type_: str,
            recipient_id: uuid.UUID,
            data: dict[str, Any],
    ) -> Notification:
        notification = Notification(type=type_, recipient_id=recipient_id, data=data)

        session.add(notification)

        return notification


def get_service(settings: NotificationsSettings) -> NotificationsDatabaseService:
    return NotificationsDatabaseService(dsn=str(settings.db_dsn))
