import pytest

from autotests.clients.rest.notifications.client import NotificationsRestClient


@pytest.mark.asyncio
async def test_health(notifications_rest_client: NotificationsRestClient):
    await notifications_rest_client.get_health()
