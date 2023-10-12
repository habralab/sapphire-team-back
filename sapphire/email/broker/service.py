import asyncio
from typing import Iterable

from facet import ServiceMixin

from sapphire.common.broker.service import BaseBrokerConsumerService
from sapphire.email.sender.service import EmailSenderService
from sapphire.email.settings import EmailSettings
from .handlers import EmailBrokerHandler


class EmailBrokerService(BaseBrokerConsumerService):
    def __init__(
            self,
            sender: EmailSenderService,
            loop: asyncio.AbstractEventLoop,
            servers: Iterable[str],
            topics: Iterable[str],
    ):
        self._sender = sender

        handlers = (
            EmailBrokerHandler(sender=sender, topics=topics),
        )
        super().__init__(loop=loop, servers=servers, topics=topics, handlers=handlers)

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._sender,
        ]

    @property
    def sender(self) -> EmailSenderService:
        return self._sender


def get_service(
        loop: asyncio.AbstractEventLoop,
        sender: EmailSenderService,
        settings: EmailSettings,
) -> EmailBrokerService:
    return EmailBrokerService(
        sender=sender,
        loop=loop,
        servers=settings.consumer_servers,
        topics=settings.topics,
    )
