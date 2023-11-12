import uuid
from typing import Type

import pytest

from autotests.clients.rest.messenger.client import MessengerRestClient
from autotests.utils import Empty


@pytest.mark.parametrize("client", (
    pytest.lazy_fixture("oleg_messenger_rest_client"),
    pytest.lazy_fixture("oleg_activated_messenger_rest_client"),
    pytest.lazy_fixture("matvey_messenger_rest_client"),
    pytest.lazy_fixture("matvey_activated_messenger_rest_client"),
))
@pytest.mark.parametrize("members", (
    {uuid.uuid4(), uuid.uuid4()},
    Empty,
))
@pytest.mark.asyncio
async def test_get_chats(client: MessengerRestClient, members: set[uuid.UUID] | Type[Empty]):
    await client.get_chats(members=members)
