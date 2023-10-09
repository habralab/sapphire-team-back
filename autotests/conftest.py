import pytest
import requests

from .settings import AutotestsSettings


@pytest.fixture
def settings() -> AutotestsSettings:
    return AutotestsSettings()


@pytest.fixture
def session():
    with requests.Session() as session:
        yield session
