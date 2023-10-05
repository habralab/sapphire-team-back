from typing import Iterable

import aiokafka
from facet import ServiceMixin
from loguru import logger

from .handler import BaseBrokerHandler


class BaseBrokerService(ServiceMixin):
    def __init__(
        self,
        servers: Iterable[str],
        topics: Iterable[str],
        handlers: Iterable[BaseBrokerHandler],
    ):
        self._handlers = handlers

        self._consumer = aiokafka.AIOKafkaConsumer(
            *topics,
            bootstrap_servers=", ".join(servers),
        )
        self._producer = aiokafka.AIOKafkaProducer(bootstrap_servers=", ".join(servers))

    async def consume(self):
        await self._consumer.start()
        try:
            async for message in self._consumer:
                await self.handle(message)
        finally:
            await self._consumer.stop()

    async def handle(self, message: aiokafka.ConsumerRecord):
        for handler in self._handlers:
            if not await handler.check(message=message):
                continue

            await handler.handle(message=message)

    async def start(self):
        logger.info("Start Broker service")

        self.add_task(self.consume())

    async def stop(self):
        logger.info("Stop Broker service")
