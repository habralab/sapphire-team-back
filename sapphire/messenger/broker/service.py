import asyncio
from typing import Iterable

from sapphire.common.api.websocket.connection_storage.storage import WebsocketConnectionStorage
from sapphire.common.broker.service import BaseBrokerConsumerService
from sapphire.messenger.broker.handler import MessengerBrokerHandler
from sapphire.messenger.database.service import MessengerDatabaseService
from sapphire.messenger.settings import MessengerSettings


class MessengerBrokerService(BaseBrokerConsumerService):
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop,
            database: MessengerDatabaseService,
            websocket_connection_storage: WebsocketConnectionStorage,
            servers: Iterable[str],
            topics: Iterable[str],
    ):
        handlers = (
            MessengerBrokerHandler(
                database=database,
                websocket_connection_storage=websocket_connection_storage,
                topics=topics,
            ),
        )
        super().__init__(loop=loop, servers=servers, topics=topics, handlers=handlers)


def get_service(
        loop: asyncio.AbstractEventLoop,
        database: MessengerDatabaseService,
        websocket_connection_storage: WebsocketConnectionStorage,
        settings: MessengerSettings,
) -> MessengerBrokerService:
    return MessengerBrokerService(
        loop=loop,
        database=database,
        websocket_connection_storage=websocket_connection_storage,
        servers=settings.consumer_servers,
        topics=settings.topics,
    )
