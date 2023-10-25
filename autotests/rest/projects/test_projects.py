import uuid
from datetime import datetime, timedelta

import pytest

from autotests.rest.projects.client.client import ProjectsRestClient


@pytest.mark.asyncio
async def test_get_projects(projects_rest_client: ProjectsRestClient):
    await projects_rest_client.get_projects()


@pytest.mark.parametrize(("client", "name", "description", "owner_id", "deadline"), (
    (
        pytest.lazy_fixture("oleg_projects_rest_client"),
        "Oleg Test Project 1",
        "Oleg Test Description 1",
        pytest.lazy_fixture("oleg_id"),
        None,
    ),
    (
        pytest.lazy_fixture("matvey_projects_rest_client"),
        "Matvey Test Project 1",
        None,
        pytest.lazy_fixture("matvey_id"),
        datetime.now() + timedelta(days=90),
    ),
))
@pytest.mark.asyncio
async def test_create_project_success(
        client: ProjectsRestClient,
        name: str,
        description: str | None,
        owner_id: uuid.UUID,
        deadline: datetime | None,
):
    project = await client.create_project(
        name=name,
        description=description,
        owner_id=owner_id,
        deadline=deadline,
    )

    assert project.name == name
    assert project.description == description
    assert project.owner_id == owner_id
    assert project.deadline == deadline
