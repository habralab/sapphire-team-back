import aiokafka


class BaseBrokerHandler:
    def __init__(self, topic: str | None = None):
        self._topic = topic

    async def check(self, message: aiokafka.ConsumerRecord) -> bool:
        if self._topic is not None and self._topic != message.topic:
            return False

        return await self.custom_check(message=message)

    async def custom_check(self, message: aiokafka.ConsumerRecord) -> bool:
        return False

    async def handle(self, message: aiokafka.ConsumerRecord):
        pass
