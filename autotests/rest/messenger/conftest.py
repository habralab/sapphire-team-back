import pytest
import requests

from autotests.settings import AutotestsSettings

from .client import MessengerRestClient


@pytest.fixture
def notifications_rest_client(
        settings: AutotestsSettings,
        session: requests.Session,
) -> MessengerRestClient:
    return MessengerRestClient(session=session, base_url=str(settings.messenger_base_url)) 
