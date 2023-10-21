import pytest
import requests

from autotests.settings import AutotestsSettings

from .client import StorageRestClient


@pytest.fixture
def users_rest_client(settings: AutotestsSettings, session: requests.Session) -> StorageRestClient:
    return StorageRestClient(session=session, base_url=str(settings.storage_base_url)) 
