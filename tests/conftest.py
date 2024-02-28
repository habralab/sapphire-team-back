import pytest

from sapphire import Settings
from sapphire.common.utils.settings import get_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings(Settings)
