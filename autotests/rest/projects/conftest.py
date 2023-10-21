import pytest

from autotests.settings import AutotestsSettings

from .client import ProjectsRestClient


@pytest.fixture
def projects_rest_client(settings: AutotestsSettings) -> ProjectsRestClient:
    return ProjectsRestClient(base_url=str(settings.projects_base_url), verify=False) 


@pytest.fixture
def user_1_projects_rest_client(
        settings: AutotestsSettings,
        user_1_access_token: str,
) -> ProjectsRestClient:
    return ProjectsRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {user_1_access_token}"},
        verify=False,
    )


@pytest.fixture
def user_2_projects_rest_client(
        settings: AutotestsSettings,
        user_2_access_token: str,
) -> ProjectsRestClient:
    return ProjectsRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {user_2_access_token}"},
        verify=False,
    )
