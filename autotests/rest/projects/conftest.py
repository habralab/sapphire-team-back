import pytest

from autotests.settings import AutotestsSettings

from .client import ProjectsRestClient


@pytest.fixture
def projects_rest_client(settings: AutotestsSettings) -> ProjectsRestClient:
    return ProjectsRestClient(base_url=str(settings.projects_base_url), verify=False) 


@pytest.fixture
def oleg_projects_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> ProjectsRestClient:
    return ProjectsRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
        verify=False,
    )


@pytest.fixture
def matvey_projects_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> ProjectsRestClient:
    return ProjectsRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
        verify=False,
    )
