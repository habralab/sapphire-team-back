from typing import Iterable

import fastapi
from facet import ServiceMixin

from sapphire.common.api.service import BaseAPIService
from sapphire.common.utils.package import get_version
from sapphire.users.database.service import UsersDatabaseService
from sapphire.users.jwt import JWTMethods
from sapphire.users.oauth2.habr import OAuth2HabrBackend
from sapphire.users.settings import UsersSettings

from .router import router


class UsersAPIService(BaseAPIService):
    def __init__(
        self,
        database: UsersDatabaseService,
        habr_oauth2: OAuth2HabrBackend,
        jwt_methods: JWTMethods,
        version: str = "0.0.0",
        root_url: str = "http://localhost",
        root_path: str = "",
        allowed_origins: Iterable[str] = (),
        port: int = 8000,
    ):
        self._database = database
        self._habr_oauth2 = habr_oauth2
        self._jwt_methods = jwt_methods

        super().__init__(
            title="Users",
            version=version,
            root_url=root_url,
            root_path=root_path,
            allowed_origins=allowed_origins,
            port=port,
        )

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

    @property
    def jwt_methods(self) -> JWTMethods:
        return self._jwt_methods


def get_service(
    database: UsersDatabaseService,
    habr_oauth2: OAuth2HabrBackend,
    jwt_methods: JWTMethods,
    settings: UsersSettings,
) -> UsersAPIService:
    return UsersAPIService(
        database=database,
        habr_oauth2=habr_oauth2,
        version=get_version() or "0.0.0",
        root_url=str(settings.root_url),
        root_path=settings.root_path,
        allowed_origins=settings.allowed_origins,
        jwt_methods=jwt_methods,
        port=settings.port,
    )
