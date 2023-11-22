import uuid
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Type

import pytest
from faker import Faker

from autotests.clients.rest.exceptions import ResponseException
from autotests.clients.rest.projects.client import ProjectsRestClient
from autotests.clients.rest.projects.enums import ProjectStatusEnum
from autotests.utils import Empty


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_projects_rest_client"),
    pytest.lazy_fixture("oleg_activated_projects_rest_client"),
    pytest.lazy_fixture("matvey_projects_rest_client"),
    pytest.lazy_fixture("matvey_activated_projects_rest_client"),
    pytest.lazy_fixture("projects_rest_client"),
    pytest.lazy_fixture("random_projects_rest_client"),
))
@pytest.mark.parametrize(
    (
        "text", "owner_id", "user_id", "startline_ge", "startline_le", "deadline_ge", "deadline_le",
        "status", "position_skill_ids", "position_specialization_ids",
        "participant_user_ids", "page", "per_page",
    ),
    (
        (Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty, 1, 10),
        (
            "test",
            uuid.uuid4(),
            uuid.uuid4(),
            datetime.utcnow(),
            datetime.utcnow() + timedelta(days=7),
            datetime.utcnow() + timedelta(days=30),
            datetime.utcnow() + timedelta(days=90),
            ProjectStatusEnum.FINISHED,
            [],
            [],
            [],
            1,
            10,
        ),
    ),
)
@pytest.mark.asyncio
async def test_get_projects(
        client: ProjectsRestClient,
        text: str | Type[Empty],
        owner_id: uuid.UUID | Type[Empty],
        user_id: uuid.UUID | Type[Empty],
        startline_ge: datetime | Type[Empty],
        startline_le: datetime | Type[Empty],
        deadline_ge: datetime | Type[Empty],
        deadline_le: datetime | Type[Empty],
        status: ProjectStatusEnum | Type[Empty],
        position_skill_ids: list[uuid.UUID] | Type[Empty],
        position_specialization_ids: list[uuid.UUID] | Type[Empty],
        participant_user_ids: list[uuid.UUID] | Type[Empty],
        page: int,
        per_page: int,
):
    projects = await client.get_projects(
        text=text,
        owner_id=owner_id,
        user_id=user_id,
        startline_ge=startline_ge,
        startline_le=startline_le,
        deadline_ge=deadline_ge,
        deadline_le=deadline_le,
        status=status,
        position_skill_ids=position_skill_ids,
        position_specialization_ids=position_specialization_ids,
        participant_user_ids=participant_user_ids,
        page=page,
        per_page=per_page,
    )

    for project in projects.data:
        if owner_id is not Empty:
            assert project.owner_id == owner_id
        if status is not Empty:
            assert project.status == status
        if startline_ge is not Empty:
            assert project.startline >= startline_ge
        if startline_le is not Empty:
            assert project.startline <= startline_le
        if deadline_ge is not Empty:
            assert project.deadline is not None and project.deadline >= deadline_ge
        if deadline_le is not Empty:
            assert project.deadline is not None and project.deadline <= deadline_le


@pytest.mark.parametrize(("client", "owner_id"), (
    (pytest.lazy_fixture("oleg_projects_rest_client"), pytest.lazy_fixture("oleg_id")),
    (pytest.lazy_fixture("matvey_projects_rest_client"), pytest.lazy_fixture("matvey_id")),
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
        await client.create_project(
            name=faker.job(),
            owner_id=owner_id,
            startline=datetime.now() + timedelta(days=30),
        )

    assert exception.value.status_code == HTTPStatus.FORBIDDEN
    assert exception.value.body == b'{"detail":"Forbidden."}'


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_projects_rest_client"),
    pytest.lazy_fixture("oleg_activated_projects_rest_client"),
    pytest.lazy_fixture("matvey_projects_rest_client"),
    pytest.lazy_fixture("matvey_activated_projects_rest_client"),
    pytest.lazy_fixture("projects_rest_client"),
    pytest.lazy_fixture("random_projects_rest_client"),
))
@pytest.mark.asyncio
async def test_get_project(project_id: uuid.UUID, client: ProjectsRestClient):
    project = await client.get_project(project_id=project_id)

    assert project.id == project_id


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_projects_rest_client"),
    pytest.lazy_fixture("oleg_activated_projects_rest_client"),
    pytest.lazy_fixture("matvey_projects_rest_client"),
    pytest.lazy_fixture("matvey_activated_projects_rest_client"),
    pytest.lazy_fixture("projects_rest_client"),
    pytest.lazy_fixture("random_projects_rest_client"),
))
@pytest.mark.asyncio
async def test_get_project_not_found(client: ProjectsRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.get_project(project_id=uuid.uuid4())

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.body == b'{"detail":"Not found."}'


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_projects_rest_client"),
    pytest.lazy_fixture("oleg_activated_projects_rest_client"),
    pytest.lazy_fixture("matvey_projects_rest_client"),
    pytest.lazy_fixture("matvey_activated_projects_rest_client"),
    pytest.lazy_fixture("projects_rest_client"),
    pytest.lazy_fixture("random_projects_rest_client"),
))
@pytest.mark.asyncio
async def test_get_project_avatar(project_id: uuid.UUID, client: ProjectsRestClient):
    await client.get_project_avatar(project_id=project_id)
