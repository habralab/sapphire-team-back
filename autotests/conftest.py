import asyncio
import datetime
import pathlib
import random
import uuid

import jwt
import pytest

from autotests.clients.email import EmailClient
from autotests.clients.rest.messenger.client import MessengerRestClient
from autotests.clients.rest.notifications.client import NotificationsRestClient
from autotests.clients.rest.projects.client import ProjectsRestClient
from autotests.clients.rest.storage.client import StorageRestClient
from autotests.clients.rest.users.client import UsersRestClient

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
def random_id(settings: AutotestsSettings) -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture(scope="session")
def oleg_email(settings: AutotestsSettings) -> str:
    return settings.oleg_email


@pytest.fixture(scope="session")
def matvey_email(settings: AutotestsSettings) -> str:
    return settings.matvey_email


@pytest.fixture(scope="session")
def project_id(settings: AutotestsSettings) -> uuid.UUID:
    return settings.project_id


@pytest.fixture(scope="session")
def position_id(settings: AutotestsSettings) -> uuid.UUID:
    return settings.position_id


@pytest.fixture(scope="session")
def participant_id(settings: AutotestsSettings) -> uuid.UUID:
    return settings.participant_id


@pytest.fixture(scope="session")
def chat_id(settings: AutotestsSettings) -> uuid.UUID:
    return settings.chat_id


@pytest.fixture(scope="session")
def oleg_notification_id(settings: AutotestsSettings) -> uuid.UUID:
    return settings.oleg_notification_id


@pytest.fixture(scope="session")
def matvey_notification_id(settings: AutotestsSettings) -> uuid.UUID:
    return settings.matvey_notification_id


@pytest.fixture(scope="session")
def backend_specialization_id() -> uuid.UUID:
    return uuid.UUID("f9b5563c-d013-40ca-861c-a4b4e66391a5")


@pytest.fixture(scope="session")
def web_design_specialization_id() -> uuid.UUID:
    return uuid.UUID("31c0da85-42b3-4f0d-9a3b-fe3c96ed241a")


@pytest.fixture(scope="session")
def git_skill_id() -> uuid.UUID:
    return uuid.UUID("1a61ae08-1426-4a22-aa90-d299c7fdeabb")


@pytest.fixture(scope="session")
def javascript_skill_id() -> uuid.UUID:
    return uuid.UUID("0a60259a-8092-47e5-9e5b-7bc53bb8ac96")


@pytest.fixture(scope="session")
def python_skill_id() -> uuid.UUID:
    return uuid.UUID("1b21c2bd-b5e2-4641-9236-2b1d0d179dc6")


@pytest.fixture(scope="session")
def uiux_design_skill_id() -> uuid.UUID:
    return uuid.UUID("78bc27b4-6ab6-49e8-9fbb-15e152edef1d")


@pytest.fixture(scope="function")
def avatar_file():
    with open(pathlib.Path(__file__).parent / "static" / "avatar.png", "rb") as avatar_file:
        yield avatar_file


@pytest.fixture(scope="session")
def oleg_access_token(settings: AutotestsSettings, oleg_id: uuid.UUID) -> str:
    payload = {
        "user_id": str(oleg_id),
        "is_activated": False,
        "exp": int(datetime.datetime.now().timestamp()) + 24 * 3600,
    }
    return jwt.encode(payload, settings.jwt_access_token_private_key, algorithm="RS256")


@pytest.fixture(scope="session")
def oleg_activated_access_token(settings: AutotestsSettings, oleg_id: uuid.UUID) -> str:
    payload = {
        "user_id": str(oleg_id),
        "is_activated": True,
        "exp": int(datetime.datetime.now().timestamp()) + 24 * 3600,
    }
    return jwt.encode(payload, settings.jwt_access_token_private_key, algorithm="RS256")


@pytest.fixture(scope="session")
def matvey_access_token(settings: AutotestsSettings, matvey_id: uuid.UUID) -> str:
    payload = {
        "user_id": str(matvey_id),
        "is_activated": False,
        "exp": int(datetime.datetime.now().timestamp()) + 24 * 3600,
    }
    return jwt.encode(payload, settings.jwt_access_token_private_key, algorithm="RS256")


@pytest.fixture(scope="session")
def matvey_activated_access_token(settings: AutotestsSettings, matvey_id: uuid.UUID) -> str:
    payload = {
        "user_id": str(matvey_id),
        "is_activated": True,
        "exp": int(datetime.datetime.now().timestamp()) + 24 * 3600,
    }
    return jwt.encode(payload, settings.jwt_access_token_private_key, algorithm="RS256")


@pytest.fixture(scope="session")
def random_access_token(settings: AutotestsSettings, random_id: uuid.UUID) -> str:
    payload = {
        "user_id": str(random_id),
        "is_activated": True,
        "exp": int(datetime.datetime.now().timestamp()) + 24 * 3600,
    }
    return jwt.encode(payload, settings.jwt_access_token_private_key, algorithm="RS256")


@pytest.fixture(scope="session")
def users_rest_client(settings: AutotestsSettings) -> UsersRestClient:
    return UsersRestClient(base_url=str(settings.users_base_url))


@pytest.fixture(scope="session")
def storage_rest_client(settings: AutotestsSettings) -> StorageRestClient:
    return StorageRestClient(base_url=str(settings.storage_base_url))


@pytest.fixture(scope="session")
def projects_rest_client(settings: AutotestsSettings) -> ProjectsRestClient:
    return ProjectsRestClient(base_url=str(settings.projects_base_url))


@pytest.fixture(scope="session")
def notifications_rest_client(settings: AutotestsSettings) -> NotificationsRestClient:
    return NotificationsRestClient(base_url=str(settings.notifications_base_url))


@pytest.fixture(scope="session")
def messenger_rest_client(settings: AutotestsSettings) -> MessengerRestClient:
    return MessengerRestClient(base_url=str(settings.messenger_base_url))


@pytest.fixture(scope="session")
def oleg_users_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> UsersRestClient:
    return UsersRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
    )


@pytest.fixture(scope="session")
def oleg_activated_users_rest_client(
        settings: AutotestsSettings,
        oleg_activated_access_token: str,
) -> UsersRestClient:
    return UsersRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {oleg_activated_access_token}"},
    )


@pytest.fixture(scope="session")
def matvey_users_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> UsersRestClient:
    return UsersRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
    )


@pytest.fixture(scope="session")
def matvey_activated_users_rest_client(
        settings: AutotestsSettings,
        matvey_activated_access_token: str,
) -> UsersRestClient:
    return UsersRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {matvey_activated_access_token}"},
    )


@pytest.fixture(scope="session")
def random_users_rest_client(settings: AutotestsSettings, random_access_token: str):
    return UsersRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {random_access_token}"},
    )


@pytest.fixture(scope="session")
def oleg_storage_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> StorageRestClient:
    return StorageRestClient(
        base_url=str(settings.storage_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
    )


@pytest.fixture(scope="session")
def oleg_activated_storage_rest_client(
        settings: AutotestsSettings,
        oleg_activated_access_token: str,
) -> StorageRestClient:
    return StorageRestClient(
        base_url=str(settings.storage_base_url),
        headers={"Authorization": f"Bearer {oleg_activated_access_token}"},
    )


@pytest.fixture(scope="session")
def matvey_storage_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> StorageRestClient:
    return StorageRestClient(
        base_url=str(settings.storage_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
    )


@pytest.fixture(scope="session")
def matvey_activated_storage_rest_client(
        settings: AutotestsSettings,
        matvey_activated_access_token: str,
) -> StorageRestClient:
    return StorageRestClient(
        base_url=str(settings.storage_base_url),
        headers={"Authorization": f"Bearer {matvey_activated_access_token}"},
    )


@pytest.fixture(scope="session")
def random_storage_rest_client(
        settings: AutotestsSettings,
        random_access_token: str,
) -> StorageRestClient:
    return StorageRestClient(
        base_url=str(settings.storage_base_url),
        headers={"Authorization": f"Bearer {random_access_token}"},
    )


@pytest.fixture(scope="session")
def oleg_projects_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> ProjectsRestClient:
    return ProjectsRestClient(
        base_url=str(settings.projects_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
    )


@pytest.fixture(scope="session")
def oleg_activated_projects_rest_client(
        settings: AutotestsSettings,
        oleg_activated_access_token: str,
) -> ProjectsRestClient:
    return ProjectsRestClient(
        base_url=str(settings.projects_base_url),
        headers={"Authorization": f"Bearer {oleg_activated_access_token}"},
    )


@pytest.fixture(scope="session")
def matvey_projects_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> ProjectsRestClient:
    return ProjectsRestClient(
        base_url=str(settings.projects_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
    )


@pytest.fixture(scope="session")
def matvey_activated_projects_rest_client(
        settings: AutotestsSettings,
        matvey_activated_access_token: str,
) -> ProjectsRestClient:
    return ProjectsRestClient(
        base_url=str(settings.projects_base_url),
        headers={"Authorization": f"Bearer {matvey_activated_access_token}"},
    )


@pytest.fixture(scope="session")
def random_projects_rest_client(
        settings: AutotestsSettings,
        random_access_token: str,
) -> ProjectsRestClient:
    return ProjectsRestClient(
        base_url=str(settings.projects_base_url),
        headers={"Authorization": f"Bearer {random_access_token}"},
    )


@pytest.fixture(scope="session")
def oleg_notifications_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> NotificationsRestClient:
    return NotificationsRestClient(
        base_url=str(settings.notifications_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
    )


@pytest.fixture(scope="session")
def oleg_activated_notifications_rest_client(
        settings: AutotestsSettings,
        oleg_activated_access_token: str,
) -> NotificationsRestClient:
    return NotificationsRestClient(
        base_url=str(settings.notifications_base_url),
        headers={"Authorization": f"Bearer {oleg_activated_access_token}"},
    )


@pytest.fixture(scope="session")
def matvey_notifications_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> NotificationsRestClient:
    return NotificationsRestClient(
        base_url=str(settings.notifications_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
    )


@pytest.fixture(scope="session")
def matvey_activated_notifications_rest_client(
        settings: AutotestsSettings,
        matvey_activated_access_token: str,
) -> NotificationsRestClient:
    return NotificationsRestClient(
        base_url=str(settings.notifications_base_url),
        headers={"Authorization": f"Bearer {matvey_activated_access_token}"},
    )


@pytest.fixture(scope="session")
def random_notifications_rest_client(
        settings: AutotestsSettings,
        random_access_token: str,
) -> NotificationsRestClient:
    return NotificationsRestClient(
        base_url=str(settings.notifications_base_url),
        headers={"Authorization": f"Bearer {random_access_token}"},
    )


@pytest.fixture(scope="session")
def oleg_messenger_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> MessengerRestClient:
    return MessengerRestClient(
        base_url=str(settings.messenger_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
    )


@pytest.fixture(scope="session")
def oleg_activated_messenger_rest_client(
        settings: AutotestsSettings,
        oleg_activated_access_token: str,
) -> MessengerRestClient:
    return MessengerRestClient(
        base_url=str(settings.messenger_base_url),
        headers={"Authorization": f"Bearer {oleg_activated_access_token}"},
    )


@pytest.fixture(scope="session")
def matvey_messenger_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> MessengerRestClient:
    return MessengerRestClient(
        base_url=str(settings.messenger_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
    )


@pytest.fixture(scope="session")
def matvey_activated_messenger_rest_client(
        settings: AutotestsSettings,
        matvey_activated_access_token: str,
) -> MessengerRestClient:
    return MessengerRestClient(
        base_url=str(settings.messenger_base_url),
        headers={"Authorization": f"Bearer {matvey_activated_access_token}"},
    )


@pytest.fixture(scope="session")
def random_messenger_rest_client(
        settings: AutotestsSettings,
        random_access_token: str,
) -> MessengerRestClient:
    return MessengerRestClient(
        base_url=str(settings.messenger_base_url),
        headers={"Authorization": f"Bearer {random_access_token}"},
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
