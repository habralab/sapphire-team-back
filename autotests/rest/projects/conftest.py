import pytest
import requests

from autotests.settings import AutotestsSettings

from .client import ProjectsRestClient


@pytest.fixture
def projects_rest_client(
        settings: AutotestsSettings,
        session: requests.Session,
) -> ProjectsRestClient:
    return ProjectsRestClient(session=session, base_url=str(settings.projects_base_url)) 
