import fastapi
import uvicorn
from facet import ServiceMixin

from sapphire.utils.uvicorn_server import UvicornServer
from .database.service import UsersDatabaseService
from .settings import UsersSettings


class UsersService(ServiceMixin):
    def __init__(self, database: UsersDatabaseService, port: int = 8000):
        self._database = database
        self._port = port

    def get_app(self) -> fastapi.FastAPI:
        return fastapi.FastAPI()

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._database,
        ]

    async def start(self):
        config = uvicorn.Config(app=self.get_app(), port=self._port)
        server = UvicornServer(config)

        self.add_task(server.serve())


def get_service(database: UsersDatabaseService, settings: UsersSettings) -> UsersService:
    return UsersService(database=database, port=settings.port)
