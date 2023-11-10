import uuid
from datetime import datetime
from http import HTTPStatus
from typing import Type

import pytest
from faker import Faker

from autotests.clients.rest.exceptions import ResponseException
from autotests.clients.rest.projects.client import ProjectsRestClient
from autotests.clients.rest.projects.enums import ProjectStatusEnum
from autotests.utils import Empty


@pytest.mark.parametrize(
    (
        "text", "owner_id", "deadline", "status", "position_is_closed",
        "position_skill_ids", "position_specialization_ids", "page", "per_page",
    ),
    (
        (Empty, Empty, Empty, Empty, Empty, Empty, Empty, 1, 10),
        (
            "test",
            uuid.uuid4(),
            datetime.utcnow(),
            ProjectStatusEnum.PREPARATION,
            False,
            [],
            [],
            1,
            10,
        ),
    ),
)
@pytest.mark.asyncio
async def test_get_projects(
        projects_rest_client: ProjectsRestClient,
        text: str | Type[Empty],
        owner_id: uuid.UUID | Type[Empty],
        deadline: datetime | Type[Empty],
        status: ProjectStatusEnum | Type[Empty],
        position_is_closed: bool | Type[Empty],
        position_skill_ids: list[uuid.UUID] | Type[Empty],
        position_specialization_ids: list[uuid.UUID] | Type[Empty],
        page: int,
        per_page: int,
):
    projects = await projects_rest_client.get_projects(
        text=text,
        owner_id=owner_id,
        deadline=deadline,
        status=status,
        position_is_closed=position_is_closed,
        position_skill_ids=position_skill_ids,
        position_specialization_ids=position_specialization_ids,
        page=page,
        per_page=per_page,
    )

    for project in projects.data:
        if owner_id is not Empty:
            assert project.owner_id == owner_id
        if status is not Empty:
            assert project.status == status


@pytest.mark.parametrize(("client", "owner_id"), (
    (pytest.lazy_fixture("oleg_projects_rest_client"), pytest.lazy_fixture("oleg_id")),
    (pytest.lazy_fixture("matvey_proejcts_rest_client"), pytest.lazy_fixture("matvey_id")),
    (pytest.lazy_fixture("oleg_projects_rest_client"), pytest.lazy_fixture("matvey_id")),
    (pytest.lazy_fixture("matvey_projects_rest_client"), pytest.lazy_fixture("oleg_id")),
    (pytest.lazy_fixture("oleg_activated_projects_rest_client"), pytest.lazy_fixture("matvey_id")),
    (pytest.lazy_fixture("matvey_activated_projects_rest_client"), pytest.lazy_fixture("oleg_id")),
))
@pytest.mark.asyncio
async def test_create_project_forbidden(
        faker: Faker,
        client: ProjectsRestClient,
        owner_id: uuid.UUID,
):
    with pytest.raises(ResponseException) as exception:
        await client.create_project(name=faker.job(), owner_id=owner_id)

    assert exception.value.status_code == HTTPStatus.FORBIDDEN
    assert exception.value.body == b'{"detail":"Forbidden."}'


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.asyncio
async def test_get_user_statistic(projects_rest_client: ProjectsRestClient, user_id: uuid.UUID):
    await projects_rest_client.get_user_statistic(user_id=user_id)
