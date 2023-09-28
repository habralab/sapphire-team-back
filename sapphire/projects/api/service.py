import fastapi
from sapphire.common.api.service import APIService
from sapphire.projects.__version__ import __version__
from sapphire.projects.settings import ProjectsSettings

from .router import router


class ProjectsAPIService(APIService):
    def __init__(self, version: str, port: int = 8000):
        super().__init__(title="Projects", version=version, port=port)

    def setup_app(self, app: fastapi.FastAPI):
        app.include_router(router, prefix="/api")


def get_service(settings: ProjectsSettings) -> ProjectsAPIService:
    return ProjectsAPIService(
        version=__version__,
        port=settings.port,
    )
