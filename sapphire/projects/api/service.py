from typing import Iterable

import fastapi

from sapphire.common.api.service import BaseAPIService
from sapphire.common.utils.package import get_version
from sapphire.projects.settings import ProjectsSettings

from . import router


class ProjectsAPIService(BaseAPIService):
    def __init__(
        self,
        version: str = "0.0.0.0",
        root_url: str = "http://localhost",
        root_path: str = "",
        allowed_origins: Iterable[str] = (),
        port: int = 8000,
    ):
        super().__init__(
            title="Projects",
            version=version,
            root_url=root_url,
            root_path=root_path,
            allowed_origins=allowed_origins,
            port=port,
        )

    def setup_app(self, app: fastapi.FastAPI):
        app.include_router(router.router, prefix="/api")


def get_service(settings: ProjectsSettings) -> ProjectsAPIService:
    return ProjectsAPIService(
        version=get_version() or "0.0.0",
        root_url=str(settings.root_url),
        root_path=settings.root_path,
        allowed_origins=settings.allowed_origins,
        port=settings.port,
    )
