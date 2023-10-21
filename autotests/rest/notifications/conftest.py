import pytest

from autotests.settings import AutotestsSettings

from .client import NotificationsRestClient


@pytest.fixture
def notifications_rest_client(settings: AutotestsSettings) -> NotificationsRestClient:
    return NotificationsRestClient(base_url=str(settings.notifications_base_url), verify=False) 


@pytest.fixture
def user_1_notifications_rest_client(
        settings: AutotestsSettings,
        user_1_access_token: str,
) -> NotificationsRestClient:
    return NotificationsRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {user_1_access_token}"},
        verify=False,
    )


@pytest.fixture
def user_2_users_rest_client(
        settings: AutotestsSettings,
        user_2_access_token: str,
) -> NotificationsRestClient:
    return NotificationsRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {user_2_access_token}"},
        verify=False,
    )
