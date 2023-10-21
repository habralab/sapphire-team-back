import pytest
import requests

from autotests.settings import AutotestsSettings

from .client import NotificationsRestClient


@pytest.fixture
def notifications_rest_client(
        settings: AutotestsSettings,
        session: requests.Session,
) -> NotificationsRestClient:
    return NotificationsRestClient(session=session, base_url=str(settings.notifications_base_url)) 
