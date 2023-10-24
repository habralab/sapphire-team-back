import pytest

from autotests.settings import AutotestsSettings

from .client import StorageRestClient


@pytest.fixture
def storage_rest_client(settings: AutotestsSettings) -> StorageRestClient:
    return StorageRestClient(base_url=str(settings.storage_base_url), verify=False) 


@pytest.fixture
def oleg_storage_rest_client(
        settings: AutotestsSettings,
        oleg_access_token: str,
) -> StorageRestClient:
    return StorageRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {oleg_access_token}"},
        verify=False,
    )


@pytest.fixture
def matvey_storage_rest_client(
        settings: AutotestsSettings,
        matvey_access_token: str,
) -> StorageRestClient:
    return StorageRestClient(
        base_url=str(settings.users_base_url),
        headers={"Authorization": f"Bearer {matvey_access_token}"},
        verify=False,
    )
