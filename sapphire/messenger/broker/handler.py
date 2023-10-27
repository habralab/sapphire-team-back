from typing import Iterable

import aiokafka

from sapphire.common.broker.handler import BaseBrokerHandler
from sapphire.common.broker.models.messenger import Chat
from sapphire.messenger.database.service import MessengerDatabaseService


class MessengerBrokerHandler(BaseBrokerHandler):
    def __init__(
            self,
            database: MessengerDatabaseService,
            topics: Iterable[str] | None = None
    ):
        self._database = database
        super().__init__(topics=topics)

    async def handle(self, message: aiokafka.ConsumerRecord):
        chat = Chat.model_validate_json(json_data=message.value)

        async with self._database.transaction() as session:
            db_chat = self._database.create_chat(
                session=session,
                is_personal=chat.is_personal
            )
        chat = Chat.model_validate(db_chat)

    @property
    def database(self) -> MessengerDatabaseService:
        return self._database
