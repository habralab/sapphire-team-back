import pytest

from collabry.common.utils.settings import get_settings
from collabry.users import Settings


@pytest.fixture()
def settings() -> Settings:
    return get_settings(Settings)
