import pytest

from collabry import Settings
from collabry.common.utils.settings import get_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings(Settings)
