from typing import Iterable

from sapphire.common.broker.service import BaseBrokerConsumerService
from sapphire.notifications.database.service import NotificationsDatabaseService
from sapphire.notifications.settings import NotificationsSettings

from .handler import NotificationsBrokerHandler


class NotificationsBrokerConsumerService(BaseBrokerConsumerService):
    def __init__(
            self,
            database: NotificationsDatabaseService,
            servers: Iterable[str],
            topics: Iterable[str],
    ):
        handlers = (
            NotificationsBrokerHandler(database=database, topics=topics),
        )

        super().__init__(servers, topics, handlers)


def get_service(
        database: NotificationsDatabaseService,
        settings: NotificationsSettings,
) -> NotificationsBrokerConsumerService:
    return NotificationsBrokerConsumerService(
        database=database,
        servers=settings.consumer_servers,
        topics=settings.topics,
    )
