import pathlib
from typing import Iterable

import fastapi
from facet import ServiceMixin

from sapphire.common.api.service import BaseAPIService
from sapphire.common.habr.client import HabrClient
from sapphire.common.jwt import JWTMethods
from sapphire.common.utils.package import get_version
from sapphire.users.database.service import UsersDatabaseService
from sapphire.users.oauth2.habr import OAuth2HabrBackend
from sapphire.users.settings import UsersSettings

from .router import router


class UsersAPIService(BaseAPIService):
    def __init__(
        self,
        database: UsersDatabaseService,
        habr_oauth2: OAuth2HabrBackend,
        habr_client: HabrClient,
        jwt_methods: JWTMethods,
        media_dir_path: pathlib.Path = pathlib.Path("/media"),
        load_file_chunk_size: int = 1024 * 1024,
        version: str = "0.0.0",
        root_url: str = "http://localhost",
        root_path: str = "",
        allowed_origins: Iterable[str] = (),
        port: int = 8000,
    ):
        self._database = database
        self._habr_oauth2 = habr_oauth2
        self._habr_client = habr_client
        self._jwt_methods = jwt_methods
        self._media_dir_path = media_dir_path
        self._load_file_chunk_size = load_file_chunk_size

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
            self._habr_oauth2,
            self._habr_client,
        ]

    @property
    def database(self) -> UsersDatabaseService:
        return self._database

    @property
    def habr_oauth2(self) -> OAuth2HabrBackend:
        return self._habr_oauth2

    @property
    def habr_client(self) -> HabrClient:
        return self._habr_client

    @property
    def jwt_methods(self) -> JWTMethods:
        return self._jwt_methods

    @property
    def media_dir_path(self) -> pathlib.Path:
        return self._media_dir_path

    @property
    def load_chunk_file_size(self) -> int:
        return self._load_file_chunk_size


def get_service(
    database: UsersDatabaseService,
    habr_oauth2: OAuth2HabrBackend,
    habr_client: HabrClient,
    jwt_methods: JWTMethods,
    settings: UsersSettings,
) -> UsersAPIService:
    return UsersAPIService(
        database=database,
        habr_oauth2=habr_oauth2,
        habr_client=habr_client,
        jwt_methods=jwt_methods,
        version=get_version() or "0.0.0",
        root_url=str(settings.root_url),
        root_path=settings.root_path,
        allowed_origins=settings.allowed_origins,
        port=settings.port,
    )
