import uuid

import pytest

from autotests.clients.rest.projects.client import ProjectsRestClient


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.asyncio
async def test_get_user_statistic(projects_rest_client: ProjectsRestClient, user_id: uuid.UUID):
    await projects_rest_client.get_user_statistic(user_id=user_id)
