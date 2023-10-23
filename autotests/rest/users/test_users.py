import uuid

import pytest

from autotests.rest.client import ResponseException
from autotests.rest.users.client.client import UsersRestClient


@pytest.mark.asyncio
async def test_get_user_full(oleg_id: uuid.UUID, oleg_users_rest_client: UsersRestClient):
    user = await oleg_users_rest_client.get_user(user_id=oleg_id)

    assert user.id == oleg_id
    assert user.email == "oleg@yurchik.space"


@pytest.mark.asyncio
async def test_get_user(matvey_id: uuid.UUID, oleg_users_rest_client: UsersRestClient):
    user = await oleg_users_rest_client.get_user(user_id=matvey_id)

    assert user.id == matvey_id
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
    assert exception.value.body == b"{}"
