import os
import pathlib
import uuid

from unittest.mock import MagicMock, AsyncMock

import pytest

from sapphire.users.database.service import UsersDatabaseService
from sapphire.users.database.models import User

AsyncSession = []


def test_get_alembic_config_path(database_service: UsersDatabaseService):
    expected_path = (
        pathlib.Path(os.curdir).absolute() / "sapphire" / "users" / "database" / "migrations"
    )

    path = database_service.get_alembic_config_path()

    assert isinstance(path, pathlib.Path)
    assert path == expected_path


@pytest.mark.asyncio
async def test_get_user(database_service: UsersDatabaseService):
    session = MagicMock()
    user_id = uuid.uuid4()
    email = "test@gmail.com"

    # Create a mock User object
    mock_user = MagicMock()
    mock_user.email = email

    # Mock the session.query().filter().first() chain to return the mock User object
    session().query().filter().first.return_value = mock_user

    user = await database_service.create_user(
        session=session,
        user_id=user_id,
        email=email,
    )

    got_user = await database_service.get_user(
        session=session,
        email=email,
    )

    assert got_user.email == email


@pytest.mark.asyncio
async def test_create_user(database_service: UsersDatabaseService):
    session = MagicMock()
    user_id = uuid.uuid4()
    email = "test@gmail.com"

    user = await database_service.create_user(
        session=session,
        user_id=user_id,
        email=email,
    )

    assert user.id == user_id
    assert user.email == email


@pytest.mark.asyncio
async def test_get_or_create_user(database_service: UsersDatabaseService):
    session = MagicMock()
    user_id = uuid.uuid4()
    email = "test@gmail.com"

    created_user = User(id=user_id, email=email)
    database_service.get_user = AsyncMock(return_value=created_user)
    database_service.create_user = AsyncMock(return_value=created_user)

    user = await database_service.get_or_create_user(
        session=session,
        user_id=user_id,
        email=email,
    )

    assert user.id is user_id
    assert user.email == email
