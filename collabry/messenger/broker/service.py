import asyncio
from typing import Iterable

from collabry.common.broker.service import BaseBrokerConsumerService
from collabry.messenger import database

from .handler import MessengerBrokerHandler
from .settings import Settings


class Service(BaseBrokerConsumerService):
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop,
            database: database.Service,
            servers: Iterable[str],
            topics: Iterable[str],
    ):
        handlers = (
            MessengerBrokerHandler(database=database, topics=topics),
        )
        super().__init__(loop=loop, servers=servers, topics=topics, handlers=handlers)


def get_service(
        loop: asyncio.AbstractEventLoop,
        database: database.Service,
        settings: Settings,
) -> Service:
    return Service(
        loop=loop,
        database=database,
        servers=settings.servers,
        topics=settings.topics,
    )
