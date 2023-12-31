import pytest

from autotests.clients.rest.messenger.client import MessengerRestClient


@pytest.mark.asyncio
async def test_health(messenger_rest_client: MessengerRestClient):
    await messenger_rest_client.get_health()
