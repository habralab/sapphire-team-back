import os
import pathlib
import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
import timezone
from sqlalchemy import desc
from sqlalchemy.future import select

from sapphire.projects.database.models import (
    Participant,
    ParticipantStatusEnum,
    Position,
    Project,
    Review,
)
from sapphire.projects.database.service import ProjectsDatabaseService


def test_get_alembic_config_path(database_service: ProjectsDatabaseService):
    expected_path = (
        pathlib.Path(os.curdir).absolute() / "sapphire" / "projects" / "database" / "migrations"
    )

    path = database_service.get_alembic_config_path()

    assert isinstance(path, pathlib.Path)
    assert path == expected_path


# Project

@pytest.mark.asyncio
async def test_create_project(database_service: ProjectsDatabaseService):
    session = MagicMock()
    name = "Any name"
    owner_id = uuid.uuid4()
    description = "Any description"
    deadline = datetime.now(tz=timezone.utc)

    project = await database_service.create_project(
        session=session,
        name=name,
        owner_id=owner_id,
        description=description,
        deadline=deadline,
    )

    assert project.name == name
    assert project.owner_id == owner_id
    assert project.description == description
    assert project.deadline == deadline

    session.add_all.assert_called_once()
    assert len(session.add_all.call_args[0]) == 1
    assert isinstance(session.add_all.call_args[0][0], list)
    assert len(session.add_all.call_args[0][0]) == 2

    session_project, session_history = session.add_all.call_args[0][0]
    assert session_project is project
    assert session_history.project is project


@pytest.mark.asyncio
async def test_get_project(database_service: ProjectsDatabaseService):
    session = MagicMock()
    result = MagicMock()
    project_id = uuid.uuid4()
    project = Project(id=project_id, name="test", owner_id=uuid.uuid4())

    result.unique.return_value.scalar_one_or_none.return_value = project
    session.execute = AsyncMock()
    session.execute.return_value = result

    result_project = await database_service.get_project(
        session=session,
        project_id=project_id,
    )

    assert result_project is project


@pytest.mark.asyncio
async def test_get_projects_without_pagination(database_service: ProjectsDatabaseService):
    session = MagicMock()
    result = MagicMock()
    project_id = uuid.uuid4()
    expected_projects = [Project(id=project_id, name="test", owner_id=uuid.uuid4())]
    expected_query = select(Project).order_by(desc(Project.created_at))
    result.unique.return_value.scalars.return_value.all.return_value = expected_projects
    session.execute = AsyncMock()
    session.execute.return_value = result

    projects = await database_service.get_projects(session=session)

    assert projects == expected_projects

    query = session.execute.call_args_list[0].args[0]
    assert expected_query.compare(query)


@pytest.mark.asyncio
async def test_get_projects_with_pagination(database_service: ProjectsDatabaseService):
    session = MagicMock()
    result = MagicMock()
    project_id = uuid.uuid4()
    expected_projects = [Project(id=project_id, name="test", owner_id=uuid.uuid4())]
    page = 1
    per_page = 10
    offset = (page - 1) * per_page
    expected_query = (
        select(Project)
        .order_by(desc(Project.created_at))
        .limit(per_page)
        .offset(offset)
    )
    result.unique.return_value.scalars.return_value.all.return_value = expected_projects
    session.execute = AsyncMock()
    session.execute.return_value = result

    projects = await database_service.get_projects(session=session, page=page, per_page=per_page)

    assert projects == expected_projects

    query = session.execute.call_args_list[0].args[0]
    assert expected_query.compare(query)


@pytest.mark.asyncio
async def test_get_projects_with_all_query_params(database_service: ProjectsDatabaseService):
    session = MagicMock()
    result = MagicMock()
    project_id = uuid.uuid4()
    owner_id = uuid.uuid4()
    deadline = datetime.utcnow()
    query_text = "query_text"
    position_skill_ids = [uuid.uuid4(), uuid.uuid4()]
    position_specialization_ids = [uuid.uuid4(), uuid.uuid4()]
    expected_projects = [Project(id=project_id, name="test", owner_id=owner_id)]
    result.unique.return_value.scalars.return_value.all.return_value = expected_projects
    session.execute = AsyncMock()
    session.execute.return_value = result

    projects = await database_service.get_projects(
        session=session,
        query_text=query_text,
        owner_id=owner_id,
        deadline=deadline,
        status=ParticipantStatusEnum.REQUEST,
        position_is_closed=False,
        position_skill_ids=position_skill_ids,
        position_specialization_ids=position_specialization_ids,
    )

    assert projects == expected_projects


# Project position

@pytest.mark.asyncio
async def test_create_project_position(database_service: ProjectsDatabaseService):
    session = MagicMock()
    project = MagicMock()
    specialization_id = uuid.uuid4()

    result_position = await database_service.create_project_position(
        session=session,
        specialization_id=specialization_id,
        project=project,
    )

    session.add.assert_called_once_with(result_position)
    assert result_position.specialization_id == specialization_id
    assert result_position.project is project


@pytest.mark.asyncio
async def test_remove_project_position(database_service: ProjectsDatabaseService):
    session = MagicMock()
    position = Position(id=uuid.uuid4(), specialization_id=uuid.uuid4(), project_id=uuid.uuid4())

    result_position = await database_service.remove_project_position(
        session=session,
        position=position,
    )

    session.add.assert_called_once_with(result_position)
    assert result_position.closed_at is not None
    assert result_position is position


@pytest.mark.asyncio
async def test_get_project_position(database_service: ProjectsDatabaseService):
    session = MagicMock()
    result = MagicMock()
    position_id = uuid.uuid4()
    position = Position(id=position_id, specialization_id=uuid.uuid4(), project_id=uuid.uuid4())

    result.unique.return_value.scalar_one_or_none.return_value = position
    session.execute = AsyncMock()
    session.execute.return_value = result

    result_position = await database_service.get_project_position(
        session=session,
        position_id=position_id,
    )

    assert result_position is position


@pytest.mark.asyncio
async def test_get_project_positions(database_service: ProjectsDatabaseService):
    session = MagicMock()
    result = MagicMock()
    project_id = uuid.uuid4()
    specialization_id = uuid.uuid4()
    expected_positions = [
        Position(id=uuid.uuid4(), specialization_id=specialization_id, project_id=project_id)
    ]
    expected_query = select(Position).where(Position.project_id == project_id)
    result.unique().scalars.return_value.all.return_value = expected_positions
    session.execute = AsyncMock()
    session.execute.return_value = result

    positions = await database_service.get_project_positions(
        session=session,
        project_id=project_id,
    )

    assert positions == expected_positions
    assert expected_query.compare(session.execute.call_args_list[0].args[0])


# Project participant

@pytest.mark.asyncio
async def test_get_participant_with_participant_id(
    database_service: ProjectsDatabaseService,
):
    session = MagicMock()
    participant_id = uuid.uuid4()
    position_id = uuid.uuid4()
    user_id = uuid.uuid4()
    expected_participant = Participant(
        id=participant_id, position_id=position_id, user_id=user_id
    )
    mock_participant = MagicMock()
    mock_participant.scalars.return_value.first.return_value = expected_participant

    session.execute = AsyncMock(return_value=mock_participant)

    participant = await database_service.get_participant(
        session=session,
        participant_id=participant_id,
    )

    assert participant is expected_participant


@pytest.mark.asyncio
async def test_get_participant_with_position_and_user_ids(
    database_service: ProjectsDatabaseService,
):
    session = MagicMock()
    participant_id = uuid.uuid4()
    position_id = uuid.uuid4()
    user_id = uuid.uuid4()
    expected_participant = Participant(
        id=participant_id, position_id=position_id, user_id=user_id
    )
    mock_participant = MagicMock()
    mock_participant.scalars.return_value.first.return_value = expected_participant

    session.execute = AsyncMock(return_value=mock_participant)

    participant = await database_service.get_participant(
        session=session,
        position_id=position_id,
        user_id=user_id,
    )

    assert participant is expected_participant


@pytest.mark.asyncio
async def test_get_participant_without_filters(
    database_service: ProjectsDatabaseService,
):
    session = MagicMock()
    position = MagicMock()
    user_id = uuid.uuid4()
    expected_participants = [Participant(position_id=position.id, user_id=user_id)]
    mock_participant = MagicMock()
    mock_participant.unique.return_value.scalars.return_value.all.return_value = expected_participants

    session.execute = AsyncMock(return_value=mock_participant)

    expected_query = select(Participant)

    participants = await database_service.get_participants(session=session)

    assert participants is expected_participants
    
    query = session.execute.call_args_list[0].args[0]
    assert expected_query.compare(query)


@pytest.mark.asyncio
async def test_get_participant_with_all_filters(
    database_service: ProjectsDatabaseService,
):
    session = MagicMock()
    project = MagicMock()
    position = MagicMock()
    user_id = uuid.uuid4()
    expected_participants = [Participant(position_id=position.id, user_id=user_id)]
    mock_participant = MagicMock()
    mock_participant.unique.return_value.scalars.return_value.all.return_value = expected_participants

    session.execute = AsyncMock(return_value=mock_participant)

    expected_query = (
        select(Participant)
        .where(
            Participant.position_id == position.id,
            Participant.user_id == user_id,
            Participant.position_id.in_(
                select(Position.id).where(Position.project_id == project.id)
            ),
        )
    )

    participants = await database_service.get_participants(
        session=session,
        project=project,
        position=position,
        user_id=user_id,
    )

    assert participants is expected_participants
    
    query = session.execute.call_args_list[0].args[0]
    assert expected_query.compare(query)


@pytest.mark.asyncio
async def test_create_participant(database_service: ProjectsDatabaseService):
    session = MagicMock()
    position_id = uuid.uuid4()
    user_id = uuid.uuid4()

    participant = await database_service.create_participant(
        session=session,
        position_id=position_id,
        user_id=user_id,
    )

    session.add.assert_called_once_with(participant)

    assert participant.position_id == position_id
    assert participant.user_id == user_id
    assert participant.status == ParticipantStatusEnum.REQUEST


@pytest.mark.asyncio
async def test_update_participant_status(database_service: ProjectsDatabaseService):
    session = MagicMock()
    position_id = uuid.uuid4()
    user_id = uuid.uuid4()
    participant = Participant(
        position_id=position_id, user_id=user_id, status=ParticipantStatusEnum.REQUEST
    )

    update_participant = await database_service.update_participant_status(
        session=session,
        participant=participant,
        status=ParticipantStatusEnum.DECLINED,
    )

    session.add.assert_called_once_with(participant)

    assert update_participant.status == ParticipantStatusEnum.DECLINED
    assert update_participant.position_id == position_id
    assert update_participant.user_id == user_id


# Reviews

async def test_create_review(database_service: ProjectsDatabaseService):
    session = MagicMock()
    project = MagicMock()
    from_user_id = uuid.uuid4()
    to_user_id = uuid.uuid4()
    rate = 5
    text = "text"

    review = await database_service.create_review(
        session=session,
        project=project,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        rate=rate,
        text=text,
    )

    session.add.assert_called_once_with(review)

    assert review.from_user_id == from_user_id
    assert review.to_user_id == to_user_id
    assert review.rate == rate
    assert review.text == text


@pytest.mark.asyncio
async def test_get_review(
    database_service: ProjectsDatabaseService,
):
    session = MagicMock()
    project = MagicMock()
    from_user_id = uuid.uuid4()
    to_user_id = uuid.uuid4()
    expected_review = Review(
        project_id=project.id,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
    )
    mock_review = MagicMock()
    mock_review.unique.return_value.scalar_one_or_none.return_value = expected_review

    expected_query = select(Review).where(
        Review.project_id == project.id,
        Review.from_user_id == from_user_id,
        Review.to_user_id == to_user_id,
    )

    session.execute = AsyncMock(return_value=mock_review)

    participant = await database_service.get_review(
        session=session,
        project=project,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
    )

    assert participant is expected_review

    query = session.execute.call_args_list[0].args[0]
    assert expected_query.compare(query)
