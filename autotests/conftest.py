import pytest

from .settings import AutotestsSettings


@pytest.fixture
def settings() -> AutotestsSettings:
    return AutotestsSettings()
