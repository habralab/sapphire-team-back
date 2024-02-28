import asyncio
from typing import Iterable

from facet import ServiceMixin

from sapphire.common.broker.service import BaseBrokerConsumerService
from sapphire.email import sender

from .handlers import SendEmailHandler
from .settings import Settings


class Service(BaseBrokerConsumerService):
    def __init__(
            self,
            sender: sender.Service,
            servers: Iterable[str],
            topics: Iterable[str],
            loop: asyncio.AbstractEventLoop | None = None,
    ):
        self._sender = sender

        handlers = (
            SendEmailHandler(sender=sender, topics=topics),
        )
        super().__init__(loop=loop, servers=servers, topics=topics, handlers=handlers)

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._sender,
        ]

    @property
    def sender(self) -> sender.Service:
        return self._sender


def get_service(
        sender: sender.Service,
        settings: Settings,
        loop: asyncio.AbstractEventLoop | None = None,
) -> Service:
    return Service(
        sender=sender,
        loop=loop,
        servers=settings.servers,
        topics=settings.topics,
    )
