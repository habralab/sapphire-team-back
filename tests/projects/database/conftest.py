import pytest

from sapphire.projects.database.service import ProjectsDatabaseService
from sapphire.projects.settings import ProjectsSettings


@pytest.fixture()
def database_service(settings: ProjectsSettings) -> ProjectsDatabaseService:
    return ProjectsDatabaseService(dsn=str(settings.database.dsn))
