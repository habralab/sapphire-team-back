import asyncio
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
def oleg_initial_user_data() -> dict[str, Any]:
    return {
        "first_name": "Oleg",
        "last_name": "Yurchik",
        "about": None,
        "main_specialization_id": None,
        "secondary_specialization_id": None,
    }


@pytest.fixture
def oleg_revert_user_data(
        loop: asyncio.AbstractEventLoop,
        oleg_initial_user_data: dict[str, Any],
        oleg_users_rest_client: UsersRestClient,
        oleg_id: uuid.UUID,
):
    yield
    loop.run_until_complete(oleg_users_rest_client.update_user(
        user_id=oleg_id,
        **oleg_initial_user_data,
    ))
