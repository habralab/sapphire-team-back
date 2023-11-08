import io
import uuid
from http import HTTPStatus

import pytest
from faker import Faker

from autotests.clients.rest.exceptions import ResponseException
from autotests.clients.rest.users.client import UsersRestClient


@pytest.mark.parametrize(("user_id", "user_email", "client"), (
    (
        pytest.lazy_fixture("oleg_id"),
        pytest.lazy_fixture("oleg_email"),
        pytest.lazy_fixture("oleg_users_rest_client"),
    ),
    (
        pytest.lazy_fixture("matvey_id"),
        pytest.lazy_fixture("matvey_email"),
        pytest.lazy_fixture("matvey_users_rest_client"),
    ),
))
@pytest.mark.asyncio
async def test_get_user_full(user_id: uuid.UUID, user_email: str, client: UsersRestClient):
    user = await client.get_user(user_id=user_id)

    assert user.id == user_id
    assert user.email == user_email


@pytest.mark.parametrize(("user_id", "client"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_users_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("users_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("random_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("random_users_rest_client")),
))
@pytest.mark.asyncio
async def test_get_user(user_id: uuid.UUID, client: UsersRestClient):
    user = await client.get_user(user_id=user_id)

    assert user.id == user_id
    assert user.email is None


@pytest.mark.parametrize(("user_id", "user_email", "client"), (
    (
        pytest.lazy_fixture("oleg_id"),
        pytest.lazy_fixture("oleg_email"),
        pytest.lazy_fixture("oleg_users_rest_client"),
    ),
    (
        pytest.lazy_fixture("matvey_id"),
        pytest.lazy_fixture("matvey_email"),
        pytest.lazy_fixture("matvey_users_rest_client"),
    ),
))
@pytest.mark.asyncio
async def test_update_user(
        faker: Faker,
        user_id: uuid.UUID,
        user_email: uuid.UUID,
        client: UsersRestClient,
):
    first_name = faker.first_name_male()
    last_name = faker.last_name_male()
    about = faker.text()
    main_specialization_id = uuid.uuid4()
    secondary_specialization_id = uuid.uuid4()

    user = await client.update_user(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        about=about,
        main_specialization_id=main_specialization_id,
        secondary_specialization_id=secondary_specialization_id,
    )

    assert user.id == user_id
    assert user.email == user_email
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.about == about
    assert user.main_specialization_id == main_specialization_id
    assert user.secondary_specialization_id == secondary_specialization_id


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.asyncio
async def test_update_user_not_authenticated(user_id: uuid.UUID, users_rest_client: UsersRestClient):
    with pytest.raises(ResponseException) as exception:
        await users_rest_client.update_user(user_id=user_id)

    assert exception.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception.value.body == b'{"detail":"Not authenticated."}'


@pytest.mark.parametrize(("user_id", "client"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_users_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("random_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("random_users_rest_client")),
))
@pytest.mark.asyncio
async def test_update_user_forbidden(user_id: uuid.UUID, client: UsersRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.update_user(user_id=user_id)

    assert exception.value.status_code == 403
    assert exception.value.body == b'{"detail":"Forbidden."}'


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_users_rest_client"),
    pytest.lazy_fixture("matvey_users_rest_client"),
    pytest.lazy_fixture("users_rest_client"),
    pytest.lazy_fixture("random_users_rest_client"),
))
@pytest.mark.asyncio
async def test_get_user_avatar(client: UsersRestClient, user_id: uuid.UUID):
    try:
        await client.get_user_avatar(user_id=user_id)
    except ResponseException as exception:
        assert exception.status_code == HTTPStatus.NOT_FOUND
        assert exception.body == b'{"detail":"Avatar not found."}'


@pytest.mark.parametrize(("user_id", "user_email", "client"), (
    (
        pytest.lazy_fixture("oleg_id"),
        pytest.lazy_fixture("oleg_email"),
        pytest.lazy_fixture("oleg_users_rest_client"),
    ),
    (
        pytest.lazy_fixture("matvey_id"),
        pytest.lazy_fixture("matvey_email"),
        pytest.lazy_fixture("matvey_users_rest_client"),
    ),
))
@pytest.mark.asyncio
async def test_update_user_avatar(
        user_id: uuid.UUID,
        user_email: str,
        client: UsersRestClient,
        avatar_file: io.BytesIO,
):
    user = await client.update_user_avatar(user_id=user_id, avatar=avatar_file)

    assert user.id == user_id
    assert user.email == user_email


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.asyncio
async def test_update_user_avatar_not_authenticated(
        user_id: uuid.UUID,
        users_rest_client: UsersRestClient,
        avatar_file: io.BytesIO,
):
    with pytest.raises(ResponseException) as exception:
        await users_rest_client.update_user_avatar(user_id=user_id, avatar=avatar_file)

    assert exception.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception.value.body == b'{"detail":"Not authenticated."}'


@pytest.mark.parametrize(("user_id", "client"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_users_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("random_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("random_users_rest_client")),
))
@pytest.mark.asyncio
async def test_update_user_avatar_forbidden(
        user_id: uuid.UUID,
        client: UsersRestClient,
        avatar_file: io.BytesIO,
):
    with pytest.raises(ResponseException) as exception:
        await client.update_user_avatar(user_id=user_id, avatar=avatar_file)

    assert exception.value.status_code == HTTPStatus.FORBIDDEN
    assert exception.value.body == b'{"detail":"Forbidden."}'


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_users_rest_client"),
    pytest.lazy_fixture("matvey_users_rest_client"),
    pytest.lazy_fixture("users_rest_client"),
    pytest.lazy_fixture("random_users_rest_client"),
))
@pytest.mark.asyncio
async def test_get_user_skills(user_id: uuid.UUID, client: UsersRestClient):
    await client.get_user_skills(user_id=user_id)


@pytest.mark.parametrize(("user_id", "client"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("oleg_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("matvey_users_rest_client")),
))
@pytest.mark.asyncio
async def test_update_user_skills(user_id: uuid.UUID, client: UsersRestClient):
    skills = {uuid.uuid4() for _ in range(10)}

    response = await client.update_user_skills(user_id=user_id, skills=skills)

    assert response == skills


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.asyncio
async def test_update_user_skills_not_authenticated(
        user_id: uuid.UUID,
        users_rest_client: UsersRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await users_rest_client.update_user_skills(user_id=user_id, skills={uuid.uuid4()})

    assert exception.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception.value.body == b'{"detail":"Not authenticated."}'


@pytest.mark.parametrize(("user_id", "client"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_users_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("random_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("random_users_rest_client")),
))
@pytest.mark.asyncio
async def test_update_user_skills_forbidden(
        user_id: uuid.UUID,
        client: UsersRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await client.update_user_skills(user_id=user_id, skills={uuid.uuid4()})

    assert exception.value.status_code == HTTPStatus.FORBIDDEN
    assert exception.value.body == b'{"detail":"Forbidden."}'
