import pytest

from autotests.clients.rest.projects.client import ProjectsRestClient


@pytest.mark.asyncio
async def test_create_review(projects_rest_client: ProjectsRestClient):
    await projects_rest_client.create_project_review()
