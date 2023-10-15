import os
import pathlib
import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from sapphire.users.database.models import Profile, User
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
    result = MagicMock()
    user_id = uuid.uuid4()
    email = "test@gmail.com"

    result.scalar_one_or_none.return_value = User(id=user_id, email=email)
    session.execute = AsyncMock()
    session.execute.return_value = result

    user = await database_service.get_user(
        session=session,
        email=email,
    )

    assert user is not None
    assert user.email == email


@pytest.mark.asyncio
async def test_create_user(database_service: UsersDatabaseService):
    session = MagicMock()
    email = "test@gmail.com"

    database_service.create_profile = AsyncMock()

    user = await database_service.create_user(
        session=session,
        email=email,
    )

    assert user.email == email

    session.add_all.assert_called_once()
    assert len(session.add_all.call_args[0]) == 1
    assert isinstance(session.add_all.call_args[0][0], list) 
    assert len(session.add_all.call_args[0][0]) == 2


@pytest.mark.asyncio
async def test_get_or_create_user_no_user(database_service: UsersDatabaseService):
    session = MagicMock()
    email = "test@gmail.com"

    created_user = User(id=uuid.uuid4(), email=email)
    database_service.get_user = AsyncMock(return_value=None)
    database_service.create_user = AsyncMock(return_value=created_user)

    user = await database_service.get_or_create_user(
        session=session,
        email=email,
    )

    assert user is created_user


@pytest.mark.asyncio
async def test_get_or_create_user_user_exists(database_service: UsersDatabaseService):
    session = MagicMock()
    email = "test@gmail.com"
    expected_user = User(id=uuid.uuid4(), email=email)

    database_service.get_user = AsyncMock(return_value=expected_user)
    database_service.create_user = AsyncMock()

    user = await database_service.get_or_create_user(
        session=session,
        email=email,
    )

    database_service.create_user.assert_not_awaited()
    assert user is expected_user


@pytest.mark.asyncio
async def test_update_user(database_service: UsersDatabaseService):
    session = MagicMock()
    user = User(id=uuid.uuid4(), email="test@gmail.com", first_name="Test", last_name="Testovich",
                avatar="/avatar.png")
    profile = Profile(user=user, main_specialization_id=uuid.uuid4(),
                      secondary_specialization_id=uuid.uuid4())
    user.profile = profile
    new_first_name = "NewTest"
    new_last_name = "NewTestovich"
    new_avatar = "/new-avatar.png"
    new_main_specialization_id = uuid.uuid4()
    new_secondary_specialization_id = uuid.uuid4()

    result_user = await database_service.update_user(
        session=session,
        user=user,
        first_name=new_first_name,
        last_name=new_last_name,
        avatar=new_avatar,
        main_specialization_id=new_main_specialization_id,
        secondary_specialization_id=new_secondary_specialization_id,
    )

    session.add_all.assert_called_once_with([user, user.profile])
    assert user is result_user
    assert result_user.first_name == new_first_name
    assert result_user.last_name == new_last_name
    assert result_user.avatar == new_avatar
    assert result_user.profile.main_specialization_id == new_main_specialization_id
    assert result_user.profile.secondary_specialization_id == new_secondary_specialization_id
