import fastapi
from facet import ServiceMixin

from sapphire.common.api.service import APIService
from sapphire.users.__version__ import __version__
from . import api
from .database.service import UsersDatabaseService
from .settings import UsersSettings


class UsersService(APIService):
    def __init__(self, database: UsersDatabaseService, version: str = "0.0.0", port: int = 8000):
        self._database = database

        super().__init__(title="Users", version=version, port=port)

    def setup_app(self, app: fastapi.FastAPI):
        app.include_router(api.router, prefix="/api")

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._database,
        ]


def get_service(database: UsersDatabaseService, settings: UsersSettings) -> UsersService:
    return UsersService(database=database, port=settings.port)
