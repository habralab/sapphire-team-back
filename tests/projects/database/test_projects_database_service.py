import os
import pathlib
import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import desc
from sqlalchemy.future import select

from sapphire.projects.database.models import (
    Participant,
    ParticipantStatusEnum,
    Position,
    Project,
    ProjectHistory,
    ProjectStatusEnum,
)
from sapphire.common.api.dependencies.pagination import PaginationModel
from sapphire.projects.database.service import ProjectsDatabaseService


def test_get_alembic_config_path(database_service: ProjectsDatabaseService):
    expected_path = (
        pathlib.Path(os.curdir).absolute() / "sapphire" / "projects" / "database" / "migrations"
    )

    path = database_service.get_alembic_config_path()

    assert isinstance(path, pathlib.Path)
    assert path == expected_path


@pytest.mark.asyncio
async def test_create_project(database_service: ProjectsDatabaseService):
    session = MagicMock()
    name = "Any name"
    owner_id = uuid.uuid4()
    description = "Any description"
    deadline = datetime.now()

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
async def test_create_project_position(database_service: ProjectsDatabaseService):
    session = MagicMock()
    name = "Position"
    project = MagicMock()

    result_position = await database_service.create_project_position(
        session=session,
        name=name,
        project=project,
    )

    session.add.assert_called_once_with(result_position)
    assert result_position.name == name
    assert result_position.project is project


@pytest.mark.asyncio
async def test_remove_project_position(database_service: ProjectsDatabaseService):
    session = MagicMock()
    position = Position(id=uuid.uuid4(), name="Position", project_id=uuid.uuid4())

    result_position = await database_service.remove_project_position(
        session=session,
        position=position,
    )

    session.add.assert_called_once_with(result_position)
    assert result_position.is_deleted is True
    assert result_position is position


@pytest.mark.asyncio
async def test_get_project_position(database_service: ProjectsDatabaseService):
    session = MagicMock()
    result = MagicMock()
    position_id = uuid.uuid4()
    position = Position(id=position_id, name="test", project_id=uuid.uuid4())

    result.unique.return_value.scalar_one_or_none.return_value = position
    session.execute = AsyncMock()
    session.execute.return_value = result

    result_position = await database_service.get_project_position(
        session=session,
        position_id=position_id,
    )

    assert result_position is position


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

    assert projects is expected_projects

    query = session.execute.call_args_list[0].args[0]
    assert expected_query.compare(query)


@pytest.mark.asyncio
async def test_get_projects_with_pagination(database_service: ProjectsDatabaseService):
    session = MagicMock()
    result = MagicMock()
    project_id = uuid.uuid4()
    expected_projects = [Project(id=project_id, name="test", owner_id=uuid.uuid4())]
    pagination = PaginationModel(page=1, per_page=10)
    offset = (pagination.page - 1) * pagination.per_page
    expected_query = (
        select(Project)
        .order_by(desc(Project.created_at))
        .limit(pagination.per_page)
        .offset(offset)
    )
    result.unique.return_value.scalars.return_value.all.return_value = expected_projects
    session.execute = AsyncMock()
    session.execute.return_value = result

    projects = await database_service.get_projects(session=session, pagination=pagination)

    assert projects is expected_projects

    query = session.execute.call_args_list[0].args[0]
    assert expected_query.compare(query)
