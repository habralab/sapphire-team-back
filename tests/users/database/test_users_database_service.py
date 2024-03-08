import os
import pathlib
import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from sapphire.database.models import Profile, User, UserSkill
from sapphire.users.database import Service


@pytest.mark.asyncio
async def test_get_user(service: Service):
    session = MagicMock()
    result = MagicMock()
    user_id = uuid.uuid4()
    email = "test@gmail.com"

    result.unique().scalar_one_or_none.return_value = User(id=user_id, email=email)
    session.execute = AsyncMock()
    session.execute.return_value = result

    user = await service.get_user(
        session=session,
        email=email,
    )

    assert user is not None
    assert user.email == email


@pytest.mark.asyncio
async def test_create_user(service: Service):
    session = MagicMock()
    email = "test@gmail.com"

    service.create_profile = AsyncMock()

    user = await service.create_user(
        session=session,
        email=email,
    )

    assert user.email == email

    session.add_all.assert_called_once()
    assert len(session.add_all.call_args[0]) == 1
    assert isinstance(session.add_all.call_args[0][0], list) 
    assert len(session.add_all.call_args[0][0]) == 2


@pytest.mark.asyncio
async def test_update_user(service: Service):
    session = MagicMock()
    user = User(id=uuid.uuid4(), email="test@gmail.com", first_name="Test", last_name="Testovich",
                avatar="/avatar.png")
    profile = Profile(user=user, main_specialization_id=uuid.uuid4(),
                      secondary_specialization_id=uuid.uuid4())
    user.profile = profile
    new_first_name = "NewTest"
    new_last_name = "NewTestovich"
    new_avatar = "/new-avatar.png"
    new_about = "New about"
    new_main_specialization_id = uuid.uuid4()
    new_secondary_specialization_id = uuid.uuid4()

    result_user = await service.update_user(
        session=session,
        user=user,
        first_name=new_first_name,
        last_name=new_last_name,
        avatar=new_avatar,
        about=new_about,
        main_specialization_id=new_main_specialization_id,
        secondary_specialization_id=new_secondary_specialization_id,
    )

    session.add_all.assert_called_once_with([user, user.profile])
    assert user is result_user
    assert result_user.first_name == new_first_name
    assert result_user.last_name == new_last_name
    assert result_user.avatar == new_avatar
    assert result_user.profile.about == new_about
    assert result_user.profile.main_specialization_id == new_main_specialization_id
    assert result_user.profile.secondary_specialization_id == new_secondary_specialization_id


@pytest.mark.asyncio
async def test_update_skills(service: Service):
    user = User(id=uuid.uuid4(), email="test@gmail.com")
    user.profile = Profile(user=user)
    user.skills = [UserSkill(user=user, skill_id=uuid.uuid4()) for _ in range(10)]
    new_skills = {uuid.uuid4() for _ in range(5)}

    session = MagicMock()

    skills = await service.update_user_skills(
        session=session,
        user=user,
        skills=new_skills,
    )
 
    assert len(session.add.call_args_list) == 2
    assert session.add.call_args_list[0].args == (user,)
    assert session.add.call_args_list[1].args == (user,)

    expected_user_skills = {(user.id, new_skill) for new_skill in new_skills}
    actual_user_skills = {(user_skill.user.id, user_skill.skill_id) for user_skill in user.skills}
    assert actual_user_skills == expected_user_skills

    assert skills is new_skills
