import pytest

from autotests.clients.rest.messenger.client import MessengerRestClient


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_messenger_rest_client"),
    pytest.lazy_fixture("oleg_activated_messenger_rest_client"),
    pytest.lazy_fixture("matvey_messenger_rest_client"),
    pytest.lazy_fixture("matvey_activated_messenger_rest_client"),
))
@pytest.mark.asyncio
async def test_get_chats(client: MessengerRestClient):
    await client.get_chats()
