import asyncio
import pathlib
import uuid
from typing import Any

import pytest

from autotests.settings import AutotestsSettings

from .client import UsersRestClient


@pytest.fixture
def users_rest_client(settings: AutotestsSettings) -> UsersRestClient:
    return UsersRestClient(base_url=str(settings.users_base_url), verify=False)


@pytest.fixture
def oleg_users_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> UsersRestClient:
    return UsersRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
        verify=False,
    )


@pytest.fixture
def matvey_users_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> UsersRestClient:
    return UsersRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
        verify=False,
    )


@pytest.fixture
def oleg_email() -> str:
    return "oleg@yurchik.space"


@pytest.fixture
def matvey_email() -> str:
    return "matveytulaevm.ama@gmail.com"


@pytest.fixture
def oleg_initial_user_data() -> dict[str, Any]:
    return {
        "first_name": "Oleg",
        "last_name": "Yurchik",
        "about": None,
        "main_specialization_id": None,
        "secondary_specialization_id": None,
    }


@pytest.fixture
def matvey_initial_user_data() -> dict[str, Any]:
    return {
        "first_name": "Matvey",
        "last_name": "Tulaev",
        "about": None,
        "main_specialization_id": None,
        "secondary_specialization_id": None,
    }


@pytest.fixture
def oleg_revert_user_data(
        event_loop: asyncio.AbstractEventLoop,
        oleg_initial_user_data: dict[str, Any],
        oleg_users_rest_client: UsersRestClient,
        oleg_id: uuid.UUID,
):
    yield
    event_loop.run_until_complete(oleg_users_rest_client.update_user(
        user_id=oleg_id,
        **oleg_initial_user_data,
    ))


@pytest.fixture
def avatar_file():
    with open(pathlib.Path(__file__).parent / "static" / "avatar.png", "rb") as f:
        yield f


@pytest.fixture
def oleg_revert_user_avatar(
        event_loop: asyncio.AbstractEventLoop,
        oleg_users_rest_client: UsersRestClient,
        oleg_id: uuid.UUID,
):
    yield
    event_loop.run_until_complete(oleg_users_rest_client.remove_user_avatar(user_id=oleg_id))


@pytest.fixture
def oleg_revert_user_skills(
        event_loop: asyncio.AbstractEventLoop,
        oleg_users_rest_client: UsersRestClient,
        oleg_id: uuid.UUID,
):
    yield
    event_loop.run_until_complete(oleg_users_rest_client.update_user_skills(
        user_id=oleg_id,
        skills=set(),
    ))
