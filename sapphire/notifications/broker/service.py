import asyncio
from typing import Iterable

from sapphire.common.broker.service import BaseBrokerConsumerService
from sapphire.notifications import database

from .handler import NotificationsBrokerHandler
from .settings import Settings


class Service(BaseBrokerConsumerService):
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop,
            database: database.Service,
            servers: Iterable[str],
            topics: Iterable[str],
    ):
        handlers = [
            NotificationsBrokerHandler(database=database, topics=topics),
        ]

        super().__init__(loop=loop, servers=servers, topics=topics, handlers=handlers)


def get_service(
        loop: asyncio.AbstractEventLoop,
        database: database.Service,
        settings: Settings,
) -> Service:
    return Service(
        loop=loop,
        database=database,
        servers=settings.consumer_servers,
        topics=settings.topics,
    )
