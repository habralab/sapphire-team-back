import uuid
from datetime import datetime, timedelta
from typing import Type

import pytest
from faker import Faker

from autotests.clients.rest.projects.enums import ParticipantStatusEnum
from autotests.utils import Empty


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_participants_rest_client"),
    pytest.lazy_fixture("oleg_activated_participants_rest_client"),
    pytest.lazy_fixture("matvey_participants_rest_client"),
    pytest.lazy_fixture("matvey_activated_participants_rest_client"),
    pytest.lazy_fixture("projects_rest_client"),
    pytest.lazy_fixture("random_projects_rest_client"),
))
@pytest.mark.parametrize(
    (
        "user_id", "position_id", "project_id", "status",
        "created_at_le", "created_at_ge", "joined_at_le", "joined_at_ge",
        "updated_at_le", "updated_at_ge", "page", "per_page",
    ),
    (
        (Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty, Empty, 1, 10),
        (
            uuid.uuid4(),
            uuid.uuid4(),
            uuid.uuid4(),
            ParticipantStatusEnum.ACTIVE,
            datetime.utcnow(),
            datetime.utcnow() - timedelta(days=30),
            datetime.utcnow(),
            datetime.utcnow() - timedelta(days=7),
            datetime.utcnow(),
            datetime.utcnow() - timedelta(days=15),
            1,
            10,
        ),
    ),
)
@pytest.mark.asyncio
async def test_get_participants(
        client: ParticipantsRestClient,
        user_id: uuid.UUID | Type[Empty],
        position_id: uuid.UUID | Type[Empty],
        project_id: uuid.UUID | Type[Empty],
        status: ParticipantStatusEnum | Type[Empty],
        created_at_le: datetime | Type[Empty],
        created_at_ge: datetime | Type[Empty],
        joined_at_le: datetime | Type[Empty],
        joined_at_ge: datetime | Type[Empty],
        updated_at_le: datetime | Type[Empty],
        updated_at_ge: datetime | Type[Empty],
        page: int,
        per_page: int,
):
    participants = await client.get_participants(
        user_id=user_id,
        position_id=position_id,
        project_id=project_id,
        status=status,
        created_at_le=created_at_le,
        created_at_ge=created_at_ge,
        joined_at_le=joined_at_le,
        joined_at_ge=joined_at_ge,
        updated_at_le=updated_at_le,
        updated_at_ge=updated_at_ge,
        page=page,
        per_page=per_page,
    )

    for participant in participants.data:
        if user_id is not Empty:
            assert participant.user_id == user_id
        if position_id is not Empty:
            assert participant.position_id == position_id
        if project_id is not Empty:
            assert participant.project_id == project_id
        if status is not Empty:
            assert participant.status == status
        if created_at_le is not Empty:
            assert participant.created_at <= created_at_le
        if created_at_ge is not Empty:
            assert participant.created_at >= created_at_ge
        if joined_at_le is not Empty:
            assert participant.joined_at <= joined_at_le
        if joined_at_ge is not Empty:
            assert participant.joined_at >= joined_at_ge
        if updated_at_le is not Empty:
            assert participant.updated_at <= updated_at_le
        if updated_at_ge is not Empty:
            assert participant.updated_at >= updated_at_ge
