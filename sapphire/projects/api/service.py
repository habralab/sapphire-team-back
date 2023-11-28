import pathlib
from typing import Iterable

import fastapi
from facet import ServiceMixin

from sapphire.common.api.service import BaseAPIService
from sapphire.common.jwt import JWTMethods
from sapphire.common.utils.package import get_version
from sapphire.projects.broker.service import ProjectsBrokerService
from sapphire.projects.database.service import ProjectsDatabaseService
from sapphire.projects.settings import ProjectsSettings
from sapphire.users.internal_api.client.service import UsersInternalAPIClient

from . import health, router


class ProjectsAPIService(BaseAPIService):
    def __init__(
        self,
        database: ProjectsDatabaseService,
        jwt_methods: JWTMethods,
        broker_service: ProjectsBrokerService,
        users_internal_api_client: UsersInternalAPIClient,
        media_dir_path: pathlib.Path = pathlib.Path("/media"),
        load_file_chunk_size: int = 1024 * 1024,  # 1 Mb
        version: str = "0.0.0.0",
        root_url: str = "http://localhost",
        root_path: str = "",
        allowed_origins: Iterable[str] = (),
        port: int = 8000,
    ):
        self._database = database
        self._jwt_methods = jwt_methods
        self._broker_service = broker_service
        self._users_internal_api_client = users_internal_api_client
        self._media_dir_path = media_dir_path
        self._load_file_chunk_size = load_file_chunk_size

        super().__init__(
            title="Projects",
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
        ]

    @property
    def database(self) -> ProjectsDatabaseService:
        return self._database

    @property
    def jwt_methods(self) -> JWTMethods:
        return self._jwt_methods

    @property
    def broker(self) -> ProjectsBrokerService:
        return self._broker_service

    @property
    def users_internal_api_client(self) -> UsersInternalAPIClient:
        return self._users_internal_api_client

    @property
    def media_dir_path(self) -> pathlib.Path:
        return self._media_dir_path

    @property
    def load_file_chunk_size(self) -> int:
        return self._load_file_chunk_size


def get_service(
        database: ProjectsDatabaseService,
        jwt_methods: JWTMethods,
        settings: ProjectsSettings,
        broker_service: ProjectsBrokerService,
        users_internal_api_client: UsersInternalAPIClient,
) -> ProjectsAPIService:
    return ProjectsAPIService(
        database=database,
        jwt_methods=jwt_methods,
        broker_service=broker_service,
        users_internal_api_client=users_internal_api_client,
        media_dir_path=settings.media_dir_path,
        load_file_chunk_size=settings.load_file_chunk_size,
        version=get_version() or "0.0.0",
        root_url=str(settings.root_url),
        root_path=settings.root_path,
        allowed_origins=settings.allowed_origins,
        port=settings.port,
    )
