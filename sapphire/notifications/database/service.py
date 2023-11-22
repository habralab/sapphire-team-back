import pathlib
import uuid
from typing import Any, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.common.utils.empty import Empty
from sapphire.notifications.settings import NotificationsSettings

from .models import Base, Notification


class NotificationsDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    def get_fixtures_directory_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "fixtures"

    def get_models(self) -> list[Type[Base]]:
        return [Notification]

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

    async def get_notifications(
            self,
            session: AsyncSession,
            recipient_id: uuid.UUID,
            is_read: bool | Type[Empty] = Empty,
            page: int | Type[Empty] = Empty,
            per_page: int | Type[Empty] = Empty,
    ) -> list[Notification]:
        filters = [Notification.recipient_id == recipient_id]
        if is_read is not Empty:
            filters.append(Notification.is_read == is_read)

        stmt = select(Notification).where(*filters)

        if page is not Empty and per_page is not Empty:
            offset = (page - 1) * per_page
            stmt = stmt.limit(per_page).offset(offset)

        result = await session.execute(stmt)

        notifications_db = list(result.scalars().all())

        return notifications_db


def get_service(settings: NotificationsSettings) -> NotificationsDatabaseService:
    return NotificationsDatabaseService(dsn=str(settings.db_dsn))
