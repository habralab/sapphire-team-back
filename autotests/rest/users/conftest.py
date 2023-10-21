import httpx
import pytest

from autotests.settings import AutotestsSettings

from .client import UsersRestClient


@pytest.fixture
def users_rest_client(settings: AutotestsSettings, client: httpx.Client) -> UsersRestClient:
    return UsersRestClient(client=client, base_url=str(settings.users_base_url)) 
