import pytest

from sapphire.storage.api.service import StorageAPIService
from sapphire.storage.database.service import StorageDatabaseService
from sapphire.storage.settings import StorageSettings


@pytest.fixture()
def settings() -> StorageSettings:
    return StorageSettings()


@pytest.fixture()
def database() -> StorageDatabaseService:
    return StorageDatabaseService()
