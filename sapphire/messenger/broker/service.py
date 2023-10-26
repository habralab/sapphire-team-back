import asyncio
from typing import Iterable

from sapphire.common.broker.service import BaseBrokerConsumerService
from sapphire.messenger.settings import MessengerSettings
from sapphire.messenger.broker.handler import MessengerBrokerHandler


class MessengerBrokerService(BaseBrokerConsumerService):
    def __init__(
            self,
            # sender: ...SenderService,
            loop: asyncio.AbstractEventLoop,
            servers: Iterable[str],
            topics: Iterable[str],
    ):
        handlers = (
            MessengerBrokerHandler(topics=topics),
        )
        super().__init__(loop=loop,
                         servers=servers,
                         topics=topics,
                         handlers=handlers)


def get_service(
        loop: asyncio.AbstractEventLoop,
        settings: MessengerSettings,
) -> EmailBrokerService:
    return EmailBrokerService(
        loop=loop,
        servers=settings.consumer_servers,
        topics=settings.topics,
    )
