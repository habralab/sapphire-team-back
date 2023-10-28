import asyncio
import datetime
import uuid

import jwt
import pytest

from autotests.clients.rest.messenger.client import MessengerRestClient
from autotests.clients.rest.notifications.client import NotificationsRestClient
from autotests.clients.rest.projects.client import ProjectsRestClient
from autotests.clients.rest.storage.client import StorageRestClient
from autotests.clients.rest.users.client import UsersRestClient

from .settings import AutotestsSettings


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def settings() -> AutotestsSettings:
    return AutotestsSettings()


@pytest.fixture(scope="session")
def oleg_id() -> uuid.UUID:
    return uuid.UUID("e23dfa16-6d0f-4de2-a1b1-a42f8a5bfd94")


@pytest.fixture(scope="session")
def matvey_id() -> uuid.UUID:
    return uuid.UUID("07dcf2a2-0a9e-4674-a5d5-8103eddcf68e")


@pytest.fixture(scope="session")
def oleg_access_token(settings: AutotestsSettings, oleg_id: uuid.UUID) -> str:
    payload = {
        "user_id": str(oleg_id),
        "exp": int(datetime.datetime.now().timestamp()) + 24 * 3600,
    }
    return jwt.encode(payload, settings.jwt_access_token_private_key, algorithm="RS256")


@pytest.fixture(scope="session")
def matvey_access_token(settings: AutotestsSettings, matvey_id: uuid.UUID) -> str:
    payload = {
        "user_id": str(matvey_id),
        "exp": int(datetime.datetime.now().timestamp()) + 24 * 3600,
    }
    return jwt.encode(payload, settings.jwt_access_token_private_key, algorithm="RS256")


@pytest.fixture(scope="session")
def users_rest_client(settings: AutotestsSettings) -> UsersRestClient:
    return UsersRestClient(base_url=str(settings.users_base_url), verify=True)


@pytest.fixture(scope="session")
def storage_rest_client(settings: AutotestsSettings) -> StorageRestClient:
    return StorageRestClient(base_url=str(settings.storage_base_url), verify=True)


@pytest.fixture(scope="session")
def projects_rest_client(settings: AutotestsSettings) -> ProjectsRestClient:
    return ProjectsRestClient(base_url=str(settings.projects_base_url), verify=True)


@pytest.fixture(scope="session")
def notifications_rest_client(settings: AutotestsSettings) -> NotificationsRestClient:
    return NotificationsRestClient(base_url=str(settings.notifications_base_url), verify=True)


@pytest.fixture(scope="session")
def messenger_rest_client(settings: AutotestsSettings) -> MessengerRestClient:
    return MessengerRestClient(base_url=str(settings.messenger_base_url), verify=True)


@pytest.fixture(scope="session")
def oleg_users_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> UsersRestClient:
    return UsersRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
        verify=True,
    )


@pytest.fixture(scope="session")
def matvey_users_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> UsersRestClient:
    return UsersRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
        verify=True,
    )


@pytest.fixture(scope="session")
def oleg_storage_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> StorageRestClient:
    return StorageRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
        verify=True,
    )


@pytest.fixture(scope="session")
def matvey_storage_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> StorageRestClient:
    return StorageRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
        verify=True,
    )


@pytest.fixture(scope="session")
def oleg_projects_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> ProjectsRestClient:
    return ProjectsRestClient(
        base_url=str(settings.projects_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
        verify=True,
    )


@pytest.fixture(scope="session")
def matvey_projects_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> ProjectsRestClient:
    return ProjectsRestClient(
        base_url=str(settings.projects_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
        verify=True,
    )


@pytest.fixture(scope="session")
def oleg_notifications_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> NotificationsRestClient:
    return NotificationsRestClient(
        base_url=str(settings.notifications_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
        verify=True,
    )


@pytest.fixture(scope="session")
def matvey_notifications_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> NotificationsRestClient:
    return NotificationsRestClient(
        base_url=str(settings.notifications_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
        verify=True,
    )



@pytest.fixture(scope="session")
def oleg_messenger_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> MessengerRestClient:
    return MessengerRestClient(
        base_url=str(settings.messenger_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
        verify=True,
    )


@pytest.fixture(scope="session")
def matvey_messenger_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> MessengerRestClient:
    return MessengerRestClient(
        base_url=str(settings.messenger_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
        verify=True,
    )
