import io
import uuid

import pytest

from autotests.rest.client import ResponseException
from autotests.rest.users.client.client import UsersRestClient


@pytest.mark.parametrize(("user_id", "user_email"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("oleg_email")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("matvey_email")),
))
@pytest.mark.asyncio
async def test_get_user_full(user_id: uuid.UUID, user_email: str, oleg_users_rest_client: UsersRestClient):
    user = await oleg_users_rest_client.get_user(user_id=user_id)

    assert user.id == user_id
    assert user.email == user_email


@pytest.mark.parametrize(("user_id", "client"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_users_rest_client")),
))
@pytest.mark.asyncio
async def test_get_user(user_id: uuid.UUID, client: UsersRestClient):
    user = await client.get_user(user_id=user_id)

    assert user.id == user_id
    assert user.email is None


@pytest.mark.parametrize(
    ("first_name", "last_name", "about", "main_specialization_id", "secondary_specialization_id"),
    (
        (
            "Kirill",
            "Mefodiev",
            "I'm a developer",
            uuid.uuid4(),
            uuid.uuid4(),
        ),
    ),
)
@pytest.mark.asyncio
async def test_update_user_success(
        oleg_revert_user_data,
        oleg_id: uuid.UUID,
        oleg_users_rest_client: UsersRestClient,
        first_name: str | None,
        last_name: str | None,
        about: str | None,
        main_specialization_id: uuid.UUID | None,
        secondary_specialization_id: uuid.UUID | None,
):
    user = await oleg_users_rest_client.update_user(
        user_id=oleg_id,
        first_name=first_name,
        last_name=last_name,
        about=about,
        main_specialization_id=main_specialization_id,
        secondary_specialization_id=secondary_specialization_id,
    )

    assert user.id == oleg_id
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.about == about
    assert user.main_specialization_id == main_specialization_id
    assert user.secondary_specialization_id == secondary_specialization_id


@pytest.mark.asyncio
async def test_update_user_forbidden(
        matvey_id: uuid.UUID,
        oleg_users_rest_client: UsersRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await oleg_users_rest_client.update_user(user_id=matvey_id)

    assert exception.value.status_code == 403
    assert exception.value.body == b'{"detail":"Forbidden"}'


@pytest.mark.asyncio
async def test_get_user_avatar(oleg_users_rest_client: UsersRestClient, oleg_id: uuid.UUID):
    try:
        await oleg_users_rest_client.get_user_avatar(user_id=oleg_id)
    except ResponseException as exception:
        assert exception.status_code == 404
        assert exception.body == b"Avatar not found."


@pytest.mark.asyncio
async def test_update_user_avatar_success(
        oleg_revert_user_avatar,
        oleg_id: uuid.UUID,
        oleg_users_rest_client: UsersRestClient,
        avatar_file: io.BytesIO,
):
    user = await oleg_users_rest_client.update_user_avatar(user_id=oleg_id, avatar=avatar_file)

    assert user.id == oleg_id


@pytest.mark.asyncio
async def test_update_user_avatar_forbidden(
        matvey_id: uuid.UUID,
        oleg_users_rest_client: UsersRestClient,
        avatar_file: io.BytesIO,
):
    with pytest.raises(ResponseException) as exception:
        await oleg_users_rest_client.update_user_avatar(user_id=matvey_id, avatar=avatar_file)

    assert exception.value.status_code == 403
    assert exception.value.body == b"{}"


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.asyncio
async def test_get_user_skills(user_id: uuid.UUID, oleg_users_rest_client: UsersRestClient):
    await oleg_users_rest_client.get_user_skills(user_id=user_id)


@pytest.mark.asyncio
async def test_update_user_skills_success(
        oleg_revert_user_skills,
        oleg_id: uuid.UUID,
        oleg_users_rest_client: UsersRestClient,
):
    skills = {uuid.uuid4() for _ in range(10)}
    response = await oleg_users_rest_client.update_user_skills(user_id=oleg_id, skills=skills)

    assert response == skills
