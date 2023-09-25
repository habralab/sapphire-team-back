from sapphire.common.database.service import DatabaseService
from sapphire.users.settings import UsersSettings


class UsersDatabaseService(DatabaseService):
    pass


def get_service(settings: UsersSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.db_dsn))
