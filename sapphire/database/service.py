import pathlib
from typing import Iterable, Type

from sapphire.common.database.service import BaseDatabaseService

from .models import MODELS, Base
from .settings import Settings


class Service(BaseDatabaseService):
    def get_migrations_directory_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    def get_fixtures_directory_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "fixtures"

    def get_models(self) -> Iterable[Type[Base]]:
        return MODELS


def get_service(settings: Settings) -> Service:
    return Service(
        dsn=str(settings.dsn),
        pool_size=settings.pool_size,
        pool_recycle=settings.pool_recycle,
    )
