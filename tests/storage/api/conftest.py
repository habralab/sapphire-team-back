import pytest

from sapphire.storage.settings import StorageSettings
from sapphire.storage.api.service import StorageAPIService
from sapphire.storage.database.service import StorageDatabaseService


@pytest.fixture()
def settings() -> StorageSettings:
    return StorageSettings()


@pytest.fixture()
def database() -> StorageDatabaseService:
    return StorageDatabaseService()
