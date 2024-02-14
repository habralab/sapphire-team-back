import pathlib
from typing import Iterable

import fastapi
from facet import ServiceMixin

from sapphire.common.api.service import BaseAPIService
from sapphire.common.habr.client import HabrClient
from sapphire.common.habr_career.client import HabrCareerClient
from sapphire.common.jwt import JWTMethods
from sapphire.common.utils.package import get_version
from sapphire.users import cache, database, oauth2

from . import health, router
from .settings import Settings


class Service(BaseAPIService):
    def __init__(
            self,
            database: database.Service,
            cache: cache.Service,
            oauth2_habr: oauth2.habr.Service,
            habr_client: HabrClient,
            habr_career_client: HabrCareerClient,
            jwt_methods: JWTMethods,
            media_dir_path: pathlib.Path = pathlib.Path("/media"),
            load_file_chunk_size: int = 1024 * 1024,
            version: str = "0.0.0",
            root_url: str = "http://localhost",
            oauth2_habr_callback_url: str = "",
            root_path: str = "",
            allowed_origins: Iterable[str] = (),
            port: int = 8000,
    ):
        self._database = database
        self._oauth2_habr = oauth2_habr
        self._oauth2_habr_callback_url = oauth2_habr_callback_url
        self._habr_client = habr_client
        self._habr_career_client = habr_career_client
        self._jwt_methods = jwt_methods
        self._media_dir_path = media_dir_path
        self._load_file_chunk_size = load_file_chunk_size
        self._cache = cache

        super().__init__(
            title="Users",
            version=version,
            root_url=root_url,
            root_path=root_path,
            allowed_origins=allowed_origins,
            port=port,
        )

    def setup_app(self, app: fastapi.FastAPI):
        app.add_api_route(path="/health", endpoint=health.health)
        app.include_router(router.router, prefix="/api")

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._database,
            self._oauth2_habr,
            self._habr_client,
            self._cache,
        ]

    @property
    def database(self) -> database.Service:
        return self._database

    @property
    def cache(self) -> cache.Service:
        return self._cache

    @property
    def jwt_methods(self) -> JWTMethods:
        return self._jwt_methods

    @property
    def oauth2_habr(self) -> oauth2.habr.Service:
        return self._oauth2_habr

    @property
    def habr_oauth2_callback_url(self) -> str:
        return self._oauth2_habr_callback_url

    @property
    def habr_client(self) -> HabrClient:
        return self._habr_client

    @property
    def habr_career_client(self) -> HabrCareerClient:
        return self._habr_career_client

    @property
    def media_dir_path(self) -> pathlib.Path:
        return self._media_dir_path

    @property
    def load_file_chunk_size(self) -> int:
        return self._load_file_chunk_size


def get_service(
        database: database.Service,
        cache: cache.Service,
        oauth2_habr: oauth2.habr.Service,
        habr_client: HabrClient,
        habr_career_client: HabrCareerClient,
        jwt_methods: JWTMethods,
        settings: Settings,
) -> Service:
    return Service(
        database=database,
        cache=cache,
        oauth2_habr=oauth2_habr,
        habr_client=habr_client,
        habr_career_client=habr_career_client,
        oauth2_habr_callback_url=settings.oauth2_habr_callback_url,
        jwt_methods=jwt_methods,
        version=get_version() or "0.0.0",
        root_url=str(settings.root_url),
        root_path=settings.root_path,
        allowed_origins=settings.allowed_origins,
        port=settings.port,
    )
