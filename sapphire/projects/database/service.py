import pathlib

from sapphire.common.database.service import BaseDatabaseService
from sapphire.projects.settings import ProjectsSettings


class ProjectsDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"


def get_service(settings: ProjectsSettings) -> ProjectsDatabaseService:
    return ProjectsDatabaseService(dsn=str(settings.db_dsn))
