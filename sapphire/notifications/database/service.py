import pathlib

from sapphire.common.database.service import BaseDatabaseService
from sapphire.notifications.settings import NotificationsSettings


class NotificationsDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"


def get_service(settings: NotificationsSettings) -> NotificationsDatabaseService:
    return NotificationsDatabaseService(dsn=str(settings.db_dsn))
