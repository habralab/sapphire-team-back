from typing import Iterable

import aiokafka

from sapphire.common.broker.handler import BaseBrokerHandler
from sapphire.notifications.database.service import NotificationsDatabaseService


class NotificationsBrokerHandler(BaseBrokerHandler):
    def __init__(self, database: NotificationsDatabaseService, topics: Iterable[str] | None = None):
        self._database = database

        super().__init__(topics=topics)

    async def handle(self, message: aiokafka.ConsumerRecord):
        pass

    @property
    def database(self) -> NotificationsDatabaseService:
        return self._database
