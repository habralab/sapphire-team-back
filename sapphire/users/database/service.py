from sapphire.database.service import DatabaseService

from .settings import UsersDatabaseSettings


class UsersDatabaseService(DatabaseService):
    pass


def get_service(settings: UsersDatabaseSettings) -> UsersDatabaseService:
    return UsersDatabaseService(dsn=str(settings.dsn))
