import os
import pathlib
import uuid
from datetime import datetime
from unittest.mock import MagicMock

import pytest

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
