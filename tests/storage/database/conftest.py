import pytest

from sapphire.storage.database.service import StorageDatabaseService
from sapphire.storage.settings import StorageSettings


@pytest.fixture()
def database_service(settings: StorageSettings) -> StorageDatabaseService:
    return StorageDatabaseService(dsn=str(settings.database.dsn))


@pytest.fixture()
def settings() -> StorageSettings:
    return StorageSettings()
