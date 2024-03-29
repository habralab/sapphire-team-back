import pytest

from collabry.common.utils.settings import get_settings
from collabry.projects import Settings


@pytest.fixture()
def settings() -> Settings:
    return get_settings(Settings)
