import pytest

from sapphire.common.utils.settings import get_settings
from sapphire.projects import Settings


@pytest.fixture()
def settings() -> Settings:
    return get_settings(Settings)
