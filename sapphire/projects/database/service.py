import pathlib
import uuid

from sapphire.common.database.service import BaseDatabaseService
from sapphire.projects.settings import ProjectsSettings

from .models import Project, ProjectHistory, ProjectStatusEnum


class ProjectsDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    async def create_project(
            self,
            name: str,
            owner_id: uuid.UUID,
            description: str | None = None,
    ) -> Project:
        project = Project(name=name, owner_id=owner_id, description=description)
        history = ProjectHistory(project=project, status=ProjectStatusEnum.preparation)

        async with self._sessionmaker() as session:
            async with session.begin():
                session.add_all([project, history])
            await session.refresh(project, attribute_names=["history"])

        return project

def get_service(settings: ProjectsSettings) -> ProjectsDatabaseService:
    return ProjectsDatabaseService(dsn=str(settings.db_dsn))
