import pytest

from sapphire.storage.settings import StorageSettings


@pytest.fixture()
def settings() -> StorageSettings:
    return StorageSettings()
