from typing import Iterable

import aiokafka

from collabry.common.broker.handler import BaseBrokerHandler
from collabry.common.broker.models.notification import Notification
from collabry.notifications.database import Service as DatabaseService


class NotificationsBrokerHandler(BaseBrokerHandler):
    def __init__(self, database: DatabaseService, topics: Iterable[str] | None = None):
        self._database = database

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

    @property
    def database(self) -> DatabaseService:
        return self._database
