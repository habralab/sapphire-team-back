import pathlib

from sapphire.common.database.service import BaseDatabaseService
from sapphire.users.settings import UsersSettings


class UsersDatabaseService(BaseDatabaseService):
    def base_get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"


def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))
