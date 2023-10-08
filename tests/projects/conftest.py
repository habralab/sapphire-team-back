import pytest

from sapphire.projects.settings import ProjectsSettings


@pytest.fixture()
def settings() -> ProjectsSettings:
    return ProjectsSettings()
