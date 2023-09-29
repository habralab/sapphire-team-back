import fastapi

from sapphire.common.api.service import APIService
from sapphire.projects.settings import ProjectsSettings

from .router import router


class ProjectsAPIService(APIService):
    def __init__(self, version: str = "0.0.0.0", port: int = 8000):
        super().__init__(title="Projects", version=version, port=port)

    def setup_app(self, app: fastapi.FastAPI):
        app.include_router(router, prefix="/api")


def get_service(settings: ProjectsSettings) -> ProjectsAPIService:
    return ProjectsAPIService(port=settings.port)
