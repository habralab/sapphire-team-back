import pytest
import requests

from autotests.settings import AutotestsSettings

from .client import UsersRestClient


@pytest.fixture
def users_rest_client(settings: AutotestsSettings, session: requests.Session) -> UsersRestClient:
    return UsersRestClient(session=session, base_url=str(settings.users_base_url)) 
