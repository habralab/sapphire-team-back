import asyncio
from typing import Iterable

import aiokafka
from loguru import logger

from sapphire.common.api.websocket.connection_storage.storage import WebsocketConnectionStorage
from sapphire.common.broker.handler import BaseBrokerHandler
from sapphire.common.broker.models.notification import Notification
from sapphire.notifications.database.service import NotificationsDatabaseService


class NotificationsBrokerHandler(BaseBrokerHandler):
    def __init__(
            self,
            database: NotificationsDatabaseService,
            websocket_connection_storage: WebsocketConnectionStorage,
            topics: Iterable[str] | None = None,
    ):
        self._database = database
        self._websocket_connection_storage = websocket_connection_storage

        super().__init__(topics=topics)

    async def handle(self, message: aiokafka.ConsumerRecord):
        notification = Notification.model_validate_json(json_data=message.value)

        async with self._database.transaction() as session:
            db_notification = self._database.create_notification(
                session=session,
                type_=notification.type,
                recipient_id=notification.recipient_id,
                data=notification.data,
            )

        notification = Notification.model_validate(db_notification)
        ws_connections = self._websocket_connection_storage.get_connections(
            user_id=notification.recipient_id,
        )
        coros = [
            logger.catch(
                ws_connection.send_json
            )(data=notification.model_dump_json())
            for ws_connection in ws_connections
        ]
        await asyncio.gather(*coros)

    @property
    def database(self) -> NotificationsDatabaseService:
        return self._database
