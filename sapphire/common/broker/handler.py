from typing import Iterable

import aiokafka


class BaseBrokerHandler:
    def __init__(self, topics: Iterable[str] | None = None):
        self._topics = topics

    async def check(self, message: aiokafka.ConsumerRecord) -> bool:
        if self._topics is not None and message.topic not in self._topics:
            return False

        return await self.custom_check(message=message)

    async def custom_check(self, message: aiokafka.ConsumerRecord) -> bool:
        return False

    async def handle(self, message: aiokafka.ConsumerRecord):
        pass
