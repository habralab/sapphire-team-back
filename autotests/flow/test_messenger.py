import uuid

import pytest
from faker import Faker

from autotests.clients.rest.messenger.client import MessengerRestClient


class TestMessageFlow:
    CONTEXT = {}

    @pytest.mark.dependency()
    @pytest.mark.asyncio
    async def test_create_chat_message(
            self,
            faker: Faker,
            chat_id: uuid.UUID,
            oleg_id: uuid.UUID,
            oleg_messenger_rest_client: MessengerRestClient,
    ):
        text = faker.text()

        message = await oleg_messenger_rest_client.create_chat_message(chat_id=chat_id, text=text)

        self.CONTEXT["message_id"] = message.id

        assert message.chat_id == chat_id
        assert message.user_id == oleg_id
        assert message.text == text

    @pytest.mark.dependency(depends=["TestMessageFlow::test_create_chat_message"])
    @pytest.mark.skip("Not implemented")
    @pytest.mark.asyncio
    async def test_get_chat_message(self):
        pass
