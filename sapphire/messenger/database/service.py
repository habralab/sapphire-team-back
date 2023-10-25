import pathlib
from typing import Type

from sapphire.common.database.service import BaseDatabaseService
from sapphire.messenger.settings import MessengerSettings

from .models import Base, Chat, Member, Message


class MessengerDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    def get_fixtures_directory_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "fixtures"

    def get_models(self) -> list[Type[Base]]:
        return [Chat, Member, Message]


def get_service(settings: MessengerSettings) -> MessengerDatabaseService:
    return MessengerDatabaseService(dsn=str(settings.db_dsn))
