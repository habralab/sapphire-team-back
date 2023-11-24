import pathlib
import uuid
from typing import Any, Type

from sqlalchemy import func, select
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

    async def _get_notifications_filters(
        self, recipient_id: uuid.UUID, is_read: bool | Type[Empty] = Empty
    ) -> list:
        filters = [Notification.recipient_id == recipient_id]
        if is_read is not Empty:
            filters.append(Notification.is_read == is_read)

        return filters

    async def get_notifications_count(
            self,
            session: AsyncSession,
            recipient_id: uuid.UUID,
            is_read: bool | Type[Empty] = Empty,
    ) -> int:
        filters = await self._get_notifications_filters(recipient_id=recipient_id, is_read=is_read)
        stmt = select(func.count(Notification.id)).where(*filters) # pylint: disable=not-callable
        result = await session.scalar(stmt)

        return result

    async def get_notifications(
            self,
            session: AsyncSession,
            recipient_id: uuid.UUID,
            is_read: bool | Type[Empty] = Empty,
            page: int = 1,
            per_page: int = 10,
    ) -> list[Notification]:
        filters = await self._get_notifications_filters(recipient_id=recipient_id, is_read=is_read)
        stmt = select(Notification).where(*filters)

        offset = (page - 1) * per_page
        stmt = stmt.limit(per_page).offset(offset)

        result = await session.execute(stmt)

        notifications_db = list(result.scalars().all())

        return notifications_db

    async def get_notification(
            self,
            session: AsyncSession,
            notification_id: uuid.UUID,
    ) -> Notification | None:
        stmt = select(Notification).where(Notification.id == notification_id)

        result = await session.execute(stmt)

        return result.unique().scalar_one_or_none()

    async def update_notification(
            self,
            session: AsyncSession,
            notification: Notification,
            is_read: bool | Type[Empty] = Empty,
    ):
        if is_read is not Empty:
            if is_read is False:
                raise ValueError("Parameter 'is_read' cannot be False")
            notification.is_read = True
        session.add(notification)


def get_service(settings: NotificationsSettings) -> NotificationsDatabaseService:
    return NotificationsDatabaseService(dsn=str(settings.db_dsn))
