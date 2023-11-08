import asyncio
import datetime
import pathlib
import random
import uuid
from typing import Any

import jwt
import pytest

from autotests.clients.email import EmailClient
from autotests.clients.rest.messenger.client import MessengerRestClient
from autotests.clients.rest.notifications.client import NotificationsRestClient
from autotests.clients.rest.projects.client import ProjectsRestClient
from autotests.clients.rest.storage.client import StorageRestClient
from autotests.clients.rest.users.client import UsersRestClient
from autotests.clients.websocket import WebsocketClient

from .settings import AutotestsSettings


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return ["ru_RU"]


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    return random.seed()


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
def oleg_id(settings: AutotestsSettings) -> uuid.UUID:
    return settings.oleg_id


@pytest.fixture(scope="session")
def matvey_id(settings: AutotestsSettings) -> uuid.UUID:
    return settings.matvey_id


@pytest.fixture(scope="session")
def oleg_email(settings: AutotestsSettings) -> str:
    return settings.oleg_email


@pytest.fixture(scope="session")
def matvey_email(settings: AutotestsSettings) -> str:
    return settings.matvey_email


@pytest.fixture(scope="session")
def oleg_initial_user_data() -> dict[str, Any]:
    return {
        "first_name": "Oleg",
        "last_name": "Yurchik",
        "about": None,
        "main_specialization_id": None,
        "secondary_specialization_id": None,
    }


@pytest.fixture(scope="session")
def matvey_initial_user_data() -> dict[str, Any]:
    return {
        "first_name": "Matvey",
        "last_name": "Tulaev",
        "about": None,
        "main_specialization_id": None,
        "secondary_specialization_id": None,
    }


@pytest.fixture(scope="function")
def avatar_file():
    with open(pathlib.Path(__file__).parent / "static" / "avatar.png", "rb") as avatar_file:
        yield avatar_file


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


@pytest.fixture(scope="session")
def oleg_messenger_websocket_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> WebsocketClient:
    return WebsocketClient(
        str(settings.messenger_websocket_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
    )


@pytest.fixture(scope="session")
def matvey_messenger_websocket_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> WebsocketClient:
    return WebsocketClient(
        str(settings.messenger_websocket_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
    )


@pytest.fixture(scope="session")
def oleg_notifications_websocket_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> WebsocketClient:
    return WebsocketClient(
        str(settings.notifications_websocket_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
    )


@pytest.fixture(scope="session")
def matvey_notifications_websocket_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> WebsocketClient:
    return WebsocketClient(
        str(settings.notifications_websocket_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
    )


@pytest.fixture(scope="session")
def oleg_email_client(settings: AutotestsSettings) -> EmailClient:
    return EmailClient(
        hostname=settings.imap_server,
        ssl=settings.imap_ssl,
        starttls=settings.imap_starttls,
        username=settings.oleg_email,
        password=settings.oleg_email_password,
    )


@pytest.fixture(scope="session")
def matvey_email_client(settings: AutotestsSettings) -> EmailClient:
    return EmailClient(
        hostname=settings.imap_server,
        ssl=settings.imap_ssl,
        starttls=settings.imap_starttls,
        username=settings.matvey_email,
        password=settings.matvey_email_password,
    )


@pytest.fixture(scope="class")
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


@pytest.fixture(scope="class")
def oleg_revert_user_avatar(
        event_loop: asyncio.AbstractEventLoop,
        oleg_users_rest_client: UsersRestClient,
        oleg_id: uuid.UUID,
):
    yield
    event_loop.run_until_complete(oleg_users_rest_client.remove_user_avatar(user_id=oleg_id))


@pytest.fixture(scope="class")
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
