import pathlib
import uuid
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from sapphire.common.database.service import BaseDatabaseService
from sapphire.projects.settings import ProjectsSettings

from .models import Project, ProjectHistory, ProjectStatusEnum


class ProjectsDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    async def create_project(
            self,
            session: AsyncSession,
            name: str,
            owner_id: uuid.UUID,
            description: str | None = None,
            deadline: datetime | None = None,
    ) -> Project:
        project = Project(name=name, owner_id=owner_id, description=description, deadline=deadline)
        history = ProjectHistory(project=project, status=ProjectStatusEnum.PREPARATION)

        session.add_all([project, history])

        return project


def get_service(settings: ProjectsSettings) -> ProjectsDatabaseService:
    return ProjectsDatabaseService(dsn=str(settings.db_dsn))
