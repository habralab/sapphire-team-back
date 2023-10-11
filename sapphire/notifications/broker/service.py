import asyncio
from typing import Iterable

from sapphire.common.api.websocket.connection_storage.storage import WebsocketConnectionStorage
from sapphire.common.broker.service import BaseBrokerConsumerService
from sapphire.notifications.database.service import NotificationsDatabaseService
from sapphire.notifications.settings import NotificationsSettings

from .handler import NotificationsBrokerHandler


class NotificationsBrokerService(BaseBrokerConsumerService):
    def __init__(
            self,
            loop: asyncio.AbstractEventLoop,
            database: NotificationsDatabaseService,
            websocket_connection_storage: WebsocketConnectionStorage,
            servers: Iterable[str],
            topics: Iterable[str],
    ):
        handlers = [
            NotificationsBrokerHandler(
                database=database,
                websocket_connection_storage=websocket_connection_storage,
                topics=topics,
            ),
        ]

        super().__init__(loop=loop, servers=servers, topics=topics, handlers=handlers)


def get_service(
        loop: asyncio.AbstractEventLoop,
        database: NotificationsDatabaseService,
        websocket_connection_storage: WebsocketConnectionStorage,
        settings: NotificationsSettings,
) -> NotificationsBrokerService:
    return NotificationsBrokerService(
        loop=loop,
        database=database,
        websocket_connection_storage=websocket_connection_storage,
        servers=settings.consumer_servers,
        topics=settings.topics,
    )
