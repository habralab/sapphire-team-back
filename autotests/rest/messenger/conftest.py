import pytest

from autotests.settings import AutotestsSettings

from .client import MessengerRestClient


@pytest.fixture
def messenger_rest_client(settings: AutotestsSettings) -> MessengerRestClient:
    return MessengerRestClient(base_url=str(settings.messenger_base_url), verify=False) 


@pytest.fixture
def user_1_messenger_rest_client(
        settings: AutotestsSettings,
        user_1_access_token: str,
) -> MessengerRestClient:
    return MessengerRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {user_1_access_token}"},
        verify=False,
    )


@pytest.fixture
def user_2_users_rest_client(
        settings: AutotestsSettings,
        user_2_access_token: str,
) -> MessengerRestClient:
    return MessengerRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {user_2_access_token}"},
        verify=False,
    )
