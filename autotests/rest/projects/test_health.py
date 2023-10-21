import pytest

from .client import ProjectsRestClient


@pytest.mark.asyncio
async def test_health(projects_rest_client: ProjectsRestClient):
    await projects_rest_client.get_health()
