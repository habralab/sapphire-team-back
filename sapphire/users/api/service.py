import fastapi
from facet import ServiceMixin

from sapphire.common.api.service import APIService
from sapphire.users.database.service import UsersDatabaseService
from sapphire.users.oauth2.habr import OAuth2HabrBackend
from sapphire.users.settings import UsersSettings

from .router import router


class UsersAPIService(APIService):
    def __init__(
            self,
            database: UsersDatabaseService,
            habr_oauth2: OAuth2HabrBackend,
            version: str = "0.0.0",
            port: int = 8000,
    ):
        self._database = database
        self._habr_oauth2 = habr_oauth2

        super().__init__(title="Users", version=version, port=port)

    def setup_app(self, app: fastapi.FastAPI):
        app.include_router(router, prefix="/api")

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._database,
        ]

    @property
    def database(self) -> UsersDatabaseService:
        return self._database

    @property
    def habr_oauth2(self) -> OAuth2HabrBackend:
        return self._habr_oauth2


def get_service(
        database: UsersDatabaseService,
        habr_oauth2: OAuth2HabrBackend,
        settings: UsersSettings,
) -> UsersAPIService:
    return UsersAPIService(
        database=database,
        habr_oauth2=habr_oauth2,
        port=settings.port,
    )
