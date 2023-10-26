from typing import Iterable

import aiokafka

from sapphire.common.broker.handler import BaseBrokerHandler
from sapphire.common.broker.models.messenger import Messegner

# from sapphire.messenger.database.service import MessengerDatabaseService


class MessengerBrokerHandler(BaseBrokerHandler):
    def __init__(self, topics: Iterable[str] | None = None):

        super().__init__(topics=topics)

    async def handle(self, message: aiokafka.ConsumerRecord):
        messenger = Messegner.model_validate_json(json_data=message.value)
