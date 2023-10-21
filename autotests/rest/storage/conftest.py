import pytest

from autotests.settings import AutotestsSettings

from .client import StorageRestClient


@pytest.fixture
def storage_rest_client(settings: AutotestsSettings) -> StorageRestClient:
    return StorageRestClient(base_url=str(settings.storage_base_url), verify=False) 


@pytest.fixture
def user_1_storage_rest_client(
        settings: AutotestsSettings,
        user_1_access_token: str,
) -> StorageRestClient:
    return StorageRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {user_1_access_token}"},
        verify=False,
    )


@pytest.fixture
def user_2_storage_rest_client(
        settings: AutotestsSettings,
        user_2_access_token: str,
) -> StorageRestClient:
    return StorageRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {user_2_access_token}"},
        verify=False,
    )
