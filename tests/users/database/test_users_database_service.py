import os
import pathlib
import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from sapphire.users.database.models import User
from sapphire.users.database.service import UsersDatabaseService


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

    async def execute_query():
        class MockQuery():
            def __init__(self):
                self.id = user_id,
                self.email = email
            def first(self):
                return User(id=self.id, email=self.email)
        return MockQuery()

    session.execute.return_value = execute_query()


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

    database_service.create_profile = AsyncMock(return_value='')

    user = await database_service.create_user(
        session=session,
        user_id=user_id,
        email=email,
    )

    assert user.id == user_id
    assert user.email == email

    session.add_all.assert_called_once()
    assert len(session.add_all.call_args[0]) == 1
    assert isinstance(session.add_all.call_args[0][0], list) 
    assert len(session.add_all.call_args[0][0]) == 2

@pytest.mark.asyncio
async def test_get_or_create_user_no_user(database_service: UsersDatabaseService):
    session = MagicMock()
    user_id = uuid.uuid4()
    email = "test@gmail.com"

    # case no user in db
    created_user = User(id=user_id, email=email)
    database_service.get_user = AsyncMock(return_value=None)
    database_service.create_user = AsyncMock(return_value=created_user)

    user = await database_service.get_or_create_user(
        session=session,
        user_id=user_id,
        email=email,
    )

    assert user.id is user_id
    assert user.email == email


@pytest.mark.asyncio
async def test_get_or_create_user_user_exists(database_service: UsersDatabaseService):
    session = MagicMock()
    user_id = uuid.uuid4()
    email = "test@gmail.com"

    created_user = User(id=user_id, email=email)

    # case user in db
    database_service.get_user = AsyncMock(return_value=created_user)
    database_service.create_user = AsyncMock(return_value='Should not be called now')

    user = await database_service.get_or_create_user(
        session=session,
        user_id=user_id,
        email=email,
    )

    assert user.id is user_id
    assert user.email == email
