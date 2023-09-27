import pathlib

from sapphire.common.database.service import DatabaseService
from sapphire.users.settings import UsersSettings


class UsersDatabaseService(DatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__)


def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))
