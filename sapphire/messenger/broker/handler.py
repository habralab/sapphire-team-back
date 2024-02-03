from typing import Iterable

import aiokafka

from sapphire.common.broker.handler import BaseBrokerHandler
from sapphire.common.broker.models.messenger import CreateChat
from sapphire.messenger import database


class MessengerBrokerHandler(BaseBrokerHandler):
    def __init__(self, database: database.Service, topics: Iterable[str] | None = None):
        self._database = database
        super().__init__(topics=topics)

    async def handle(self, message: aiokafka.ConsumerRecord):
        chat = CreateChat.model_validate_json(json_data=message.value)
        async with self._database.transaction() as session:
            await self._database.create_chat(
                session=session,
                is_personal=chat.is_personal,
                members_ids=chat.members_ids
            )

    @property
    def database(self) -> database.Service:
        return self._database
