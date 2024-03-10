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
    (
        pytest.lazy_fixture("oleg_id"),
        pytest.lazy_fixture("oleg_email"),
        pytest.lazy_fixture("oleg_activated_users_rest_client"),
    ),
    (
        pytest.lazy_fixture("matvey_id"),
        pytest.lazy_fixture("matvey_email"),
        pytest.lazy_fixture("matvey_activated_users_rest_client"),
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
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_activated_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_activated_users_rest_client")),
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


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_users_rest_client"),
    pytest.lazy_fixture("matvey_users_rest_client"),
    pytest.lazy_fixture("oleg_activated_users_rest_client"),
    pytest.lazy_fixture("matvey_activated_users_rest_client"),
    pytest.lazy_fixture("users_rest_client"),
    pytest.lazy_fixture("random_users_rest_client"),
))
@pytest.mark.asyncio
async def test_get_user_not_found(client: UsersRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.get_user(user_id=uuid.uuid4())

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.body == b'{"detail":"Not found."}'


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
    (
        pytest.lazy_fixture("oleg_id"),
        pytest.lazy_fixture("oleg_email"),
        pytest.lazy_fixture("oleg_activated_users_rest_client"),
    ),
    (
        pytest.lazy_fixture("matvey_id"),
        pytest.lazy_fixture("matvey_email"),
        pytest.lazy_fixture("matvey_activated_users_rest_client"),
    ),
))
@pytest.mark.asyncio
async def test_update_user(
        faker: Faker,
        user_id: uuid.UUID,
        user_email: uuid.UUID,
        backend_specialization_id: uuid.UUID,
        web_design_specialization_id: uuid.UUID,
        client: UsersRestClient,
):
    first_name = faker.first_name_male()
    last_name = faker.last_name_male()
    about = faker.text()

    user = await client.update_user(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        about=about,
        main_specialization_id=backend_specialization_id,
        secondary_specialization_id=web_design_specialization_id,
    )

    assert user.id == user_id
    assert user.email == user_email
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.about == about
    assert user.main_specialization_id == backend_specialization_id
    assert user.secondary_specialization_id == web_design_specialization_id


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.asyncio
async def test_update_user_not_authenticated(
        faker: Faker,
        user_id: uuid.UUID,
        users_rest_client: UsersRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await users_rest_client.update_user(
            user_id=user_id,
            first_name=faker.first_name(),
            last_name=faker.last_name(),
        )

    assert exception.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception.value.body == b'{"detail":"Not authenticated."}'


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_users_rest_client"),
    pytest.lazy_fixture("oleg_activated_users_rest_client"),
    pytest.lazy_fixture("matvey_users_rest_client"),
    pytest.lazy_fixture("matvey_activated_users_rest_client"),
))
@pytest.mark.asyncio
async def test_update_user_not_found(faker: Faker, client: UsersRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.update_user(
            user_id=uuid.uuid4(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
        )

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.body == b'{"detail":"Not found."}'


@pytest.mark.parametrize(("user_id", "client"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_users_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_activated_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_activated_users_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("random_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("random_users_rest_client")),
))
@pytest.mark.asyncio
async def test_update_user_forbidden(faker: Faker, user_id: uuid.UUID, client: UsersRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.update_user(
            user_id=user_id,
            first_name=faker.first_name(),
            last_name=faker.last_name(),
        )

    assert exception.value.status_code == 403
    assert exception.value.body == b'{"detail":"Forbidden."}'


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_users_rest_client"),
    pytest.lazy_fixture("oleg_activated_users_rest_client"),
    pytest.lazy_fixture("matvey_users_rest_client"),
    pytest.lazy_fixture("matvey_activated_users_rest_client"),
    pytest.lazy_fixture("users_rest_client"),
    pytest.lazy_fixture("random_users_rest_client"),
))
@pytest.mark.asyncio
async def test_get_user_avatar(client: UsersRestClient, user_id: uuid.UUID):
    await client.get_user_avatar(user_id=user_id)


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_users_rest_client"),
    pytest.lazy_fixture("oleg_activated_users_rest_client"),
    pytest.lazy_fixture("matvey_users_rest_client"),
    pytest.lazy_fixture("matvey_activated_users_rest_client"),
    pytest.lazy_fixture("users_rest_client"),
    pytest.lazy_fixture("random_users_rest_client"),
))
@pytest.mark.asyncio
async def test_get_user_avatar_not_found(client: UsersRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.get_user_avatar(user_id=uuid.uuid4())

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.body == b'{"detail":"Not found."}'


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
    (
        pytest.lazy_fixture("oleg_id"),
        pytest.lazy_fixture("oleg_email"),
        pytest.lazy_fixture("oleg_activated_users_rest_client"),
    ),
    (
        pytest.lazy_fixture("matvey_id"),
        pytest.lazy_fixture("matvey_email"),
        pytest.lazy_fixture("matvey_activated_users_rest_client"),
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


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_users_rest_client"),
    pytest.lazy_fixture("oleg_activated_users_rest_client"),
    pytest.lazy_fixture("matvey_users_rest_client"),
    pytest.lazy_fixture("matvey_activated_users_rest_client"),
))
@pytest.mark.asyncio
async def test_update_user_avatar_not_found(avatar_file: io.BytesIO, client: UsersRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.update_user_avatar(user_id=uuid.uuid4(), avatar=avatar_file)

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.body == b'{"detail":"Not found."}'


@pytest.mark.parametrize(("user_id", "client"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_users_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_activated_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_activated_users_rest_client")),
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


@pytest.mark.parametrize(("user_id", "email", "client"), (
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
    (
        pytest.lazy_fixture("oleg_id"),
        pytest.lazy_fixture("oleg_email"),
        pytest.lazy_fixture("oleg_activated_users_rest_client"),
    ),
    (
        pytest.lazy_fixture("matvey_id"),
        pytest.lazy_fixture("matvey_email"),
        pytest.lazy_fixture("matvey_activated_users_rest_client"),
    ),
))
@pytest.mark.asyncio
async def test_remove_user_avatar(user_id: uuid.UUID, email: str, client: UsersRestClient):
    user = await client.remove_user_avatar(user_id=user_id)

    assert user.id == user_id
    assert user.email == email


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.asyncio
async def test_remove_user_avatar_not_authenticated(
        user_id: uuid.UUID,
        users_rest_client: UsersRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await users_rest_client.remove_user_avatar(user_id=user_id)

    assert exception.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception.value.body == b'{"detail":"Not authenticated."}'


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_users_rest_client"),
    pytest.lazy_fixture("oleg_activated_users_rest_client"),
    pytest.lazy_fixture("matvey_users_rest_client"),
    pytest.lazy_fixture("matvey_activated_users_rest_client"),
))
@pytest.mark.asyncio
async def test_remove_user_avatar_not_found(client: UsersRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.remove_user_avatar(user_id=uuid.uuid4())

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.body == b'{"detail":"Not found."}'


@pytest.mark.parametrize(("user_id", "client"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_users_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_activated_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_activated_users_rest_client")),
))
@pytest.mark.asyncio
async def test_remove_user_avatar_forbidden(user_id: uuid.UUID, client: UsersRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.remove_user_avatar(user_id=user_id)

    assert exception.value.status_code == HTTPStatus.FORBIDDEN
    assert exception.value.body == b'{"detail":"Forbidden."}'


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_users_rest_client"),
    pytest.lazy_fixture("oleg_activated_users_rest_client"),
    pytest.lazy_fixture("matvey_users_rest_client"),
    pytest.lazy_fixture("matvey_activated_users_rest_client"),
    pytest.lazy_fixture("users_rest_client"),
    pytest.lazy_fixture("random_users_rest_client"),
))
@pytest.mark.asyncio
async def test_get_user_skills(user_id: uuid.UUID, client: UsersRestClient):
    await client.get_user_skills(user_id=user_id)


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_users_rest_client"),
    pytest.lazy_fixture("oleg_activated_users_rest_client"),
    pytest.lazy_fixture("matvey_users_rest_client"),
    pytest.lazy_fixture("matvey_activated_users_rest_client"),
    pytest.lazy_fixture("users_rest_client"),
    pytest.lazy_fixture("random_users_rest_client"),
))
@pytest.mark.asyncio
async def test_get_user_skills_not_found(client: UsersRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.get_user_skills(user_id=uuid.uuid4())

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.body == b'{"detail":"Not found."}'


@pytest.mark.parametrize(("user_id", "client"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("oleg_users_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("oleg_activated_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("matvey_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("matvey_activated_users_rest_client")),
))
@pytest.mark.asyncio
async def test_update_user_skills(
        user_id: uuid.UUID,
        client: UsersRestClient,
        git_skill_id: uuid.UUID,
        javascript_skill_id: uuid.UUID,
        uiux_design_skill_id: uuid.UUID,
):
    skills = {git_skill_id, javascript_skill_id, uiux_design_skill_id}

    response = await client.update_user_skills(user_id=user_id, skills=skills)

    assert response == skills


@pytest.mark.parametrize("user_id", (
    pytest.lazy_fixture("oleg_id"),
    pytest.lazy_fixture("matvey_id"),
))
@pytest.mark.asyncio
async def test_update_user_skills_not_authenticated(
        user_id: uuid.UUID,
        git_skill_id: uuid.UUID,
        users_rest_client: UsersRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await users_rest_client.update_user_skills(user_id=user_id, skills={git_skill_id})

    assert exception.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exception.value.body == b'{"detail":"Not authenticated."}'


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_users_rest_client"),
    pytest.lazy_fixture("oleg_activated_users_rest_client"),
    pytest.lazy_fixture("matvey_users_rest_client"),
    pytest.lazy_fixture("matvey_activated_users_rest_client"),
))
@pytest.mark.asyncio
async def test_update_user_skills_not_found(client: UsersRestClient):
    with pytest.raises(ResponseException) as exception:
        await client.update_user_skills(user_id=uuid.uuid4(), skills=set())

    assert exception.value.status_code == HTTPStatus.NOT_FOUND
    assert exception.value.body == b'{"detail":"Not found."}'


@pytest.mark.parametrize(("user_id", "client"), (
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_users_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("matvey_activated_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("oleg_activated_users_rest_client")),
    (pytest.lazy_fixture("oleg_id"), pytest.lazy_fixture("random_users_rest_client")),
    (pytest.lazy_fixture("matvey_id"), pytest.lazy_fixture("random_users_rest_client")),
))
@pytest.mark.asyncio
async def test_update_user_skills_forbidden(
        user_id: uuid.UUID,
        python_skill_id: uuid.UUID,
        client: UsersRestClient,
):
    with pytest.raises(ResponseException) as exception:
        await client.update_user_skills(user_id=user_id, skills={python_skill_id})

    assert exception.value.status_code == HTTPStatus.FORBIDDEN
    assert exception.value.body == b'{"detail":"Forbidden."}'
