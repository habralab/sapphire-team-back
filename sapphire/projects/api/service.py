from typing import Iterable

import fastapi
from facet import ServiceMixin

from sapphire.common.api.service import BaseAPIService
from sapphire.common.jwt import JWTMethods
from sapphire.common.utils.package import get_version
from sapphire.projects.database.service import ProjectsDatabaseService
from sapphire.projects.settings import ProjectsSettings

from . import health, router


class ProjectsAPIService(BaseAPIService):
    def __init__(
        self,
        database: ProjectsDatabaseService,
        jwt_methods: JWTMethods,
        version: str = "0.0.0.0",
        root_url: str = "http://localhost",
        root_path: str = "",
        allowed_origins: Iterable[str] = (),
        port: int = 8000,
    ):
        self._database = database
        self._jwt_methods = jwt_methods

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


def get_service(
        database: ProjectsDatabaseService,
        jwt_methods: JWTMethods,
        settings: ProjectsSettings,
) -> ProjectsAPIService:
    return ProjectsAPIService(
        database=database,
        jwt_methods=jwt_methods,
        version=get_version() or "0.0.0",
        root_url=str(settings.root_url),
        root_path=settings.root_path,
        allowed_origins=settings.allowed_origins,
        port=settings.port,
    )
