import asyncio
from typing import Iterable

from sapphire.common.broker.service import BaseBrokerConsumerService
from sapphire.messenger.broker.handler import MessengerBrokerHandler
from sapphire.messenger.database.service import MessengerDatabaseService
from sapphire.messenger.settings import MessengerSettings


class MessengerBrokerService(BaseBrokerConsumerService):
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop,
            database: MessengerDatabaseService,
            servers: Iterable[str],
            topics: Iterable[str],
    ):
        handlers = (
            MessengerBrokerHandler(topics=topics, database=database),
        )
        super().__init__(
            loop=loop,
            servers=servers,
            topics=topics,
            handlers=handlers
            )


def get_service(
        loop: asyncio.AbstractEventLoop,
        settings: MessengerSettings,
        database: MessengerDatabaseService
) -> MessengerBrokerService:
    return MessengerBrokerService(
        loop=loop,
        servers=settings.consumer_servers,
        topics=settings.topics,
        database=database
        )
