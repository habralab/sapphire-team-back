import uuid
from datetime import datetime, timedelta
from typing import Type

import pytest
from autotests.clients.rest.projects.client import ProjectsRestClient
from autotests.clients.rest.projects.models import ProjectStatusEnum
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
    ("project_id", "is_closed", "specialization_ids", "skill_ids", "project_query_text",
     "project_startline_ge", "project_startline_le", "project_deadline_ge", "project_deadline_le",
     "project_status", "page", "per_page"),
    (
        (Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty, 1, 10),
        (
            Empty,
            False,
            [uuid.uuid4(), uuid.uuid4()],
            [uuid.uuid4(), uuid.uuid4()],
            "test",
            datetime.now() - timedelta(days=30),
            datetime.now() + timedelta(days=30),
            datetime.now() + timedelta(days=30),
            datetime.now() + timedelta(days=90),
            ProjectStatusEnum.PREPARATION,
            1,
            10,
        ),
    ),
)
@pytest.mark.asyncio
async def test_get_positions(
        client: ProjectsRestClient,
        project_id: uuid.UUID | Type[Empty],
        is_closed: bool | Type[Empty],
        specialization_ids: list[uuid.UUID] | Type[Empty],
        skill_ids: list[uuid.UUID] | Type[Empty],
        project_query_text: str | Type[Empty],
        project_startline_ge: datetime | Type[Empty],
        project_startline_le: datetime | Type[Empty],
        project_deadline_ge: datetime | Type[Empty],
        project_deadline_le: datetime | Type[Empty],
        project_status: ProjectStatusEnum | Type[Empty],
        page: int,
        per_page: int,
):
    positions = await client.get_positions(
        project_id=project_id,
        is_closed=is_closed,
        specialization_ids=specialization_ids,
        skill_ids=skill_ids,
        project_query_text=project_query_text,
        project_startline_ge=project_startline_ge,
        project_startline_le=project_startline_le,
        project_deadline_ge=project_deadline_ge,
        project_deadline_le=project_deadline_le,
        project_status=project_status,
        page=page,
        per_page=per_page,
    )

    for position in positions.data:
        if is_closed is not Empty:
            assert (position.closed_at is not None) == is_closed
        if specialization_ids is not Empty:
            assert position.specialization_id in specialization_ids
