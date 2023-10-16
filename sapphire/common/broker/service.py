import asyncio
import json
from typing import Any, Iterable

import aiokafka
import backoff
from facet import ServiceMixin
from loguru import logger

from .handler import BaseBrokerHandler


class BaseBrokerConsumerService(ServiceMixin):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        servers: Iterable[str],
        topics: Iterable[str],
        handlers: Iterable[BaseBrokerHandler] = (),
    ):
        self._handlers = handlers

        self._consumer = aiokafka.AIOKafkaConsumer(
            *topics,
            loop=loop,
            bootstrap_servers=",".join(servers),
        )

    @backoff.on_exception(backoff.expo, Exception)
    async def consume(self):
        await self._consumer.start()
        try:
            async for message in self._consumer:
                logger.debug("Get message from '{}': {}", message.topic, message.value)
                await self.handle(message)
        finally:
            await self._consumer.stop()

    async def handle(self, message: aiokafka.ConsumerRecord):
        for handler in self._handlers:
            if not await handler.check(message=message):
                logger.debug("Skip message from '{}': {}", message.topic, message.value)
                continue

            logger.debug("Handle message from '{}': {}", message.topic, message.value)
            await handler.handle(message=message)

    async def start(self):
        logger.info("Start Broker Consumer service")

        self.add_task(self.consume())

    async def stop(self):
        logger.info("Stop Broker Consumer service")


class BaseBrokerProducerService(ServiceMixin):
    def __init__(self, loop: asyncio.AbstractEventLoop, servers: Iterable[str]):
        self._producer = aiokafka.AIOKafkaProducer(loop=loop, bootstrap_servers=",".join(servers))

    async def send(self, topic: str, message: dict[str, Any]):
        payload = json.dumps(message).encode()

        await self._producer.send_and_wait(topic=topic, value=payload)

        logger.debug("Send message to '{}': {}", topic, payload)

    async def start(self):
        logger.info("Start Broker Producer service")

        await self._producer.start()

    async def stop(self):
        logger.info("Stop Broker Producer service")

        await self._producer.stop()
