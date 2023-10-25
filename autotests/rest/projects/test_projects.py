import pytest

from autotests.clients.rest.projects.client import ProjectsRestClient


@pytest.mark.asyncio
async def test_get_projects(projects_rest_client: ProjectsRestClient):
    await projects_rest_client.get_projects()
