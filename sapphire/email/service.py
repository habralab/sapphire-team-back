import asyncio

from facet import ServiceMixin

from . import broker, sender
from .settings import Settings


class Service(ServiceMixin):
    def __init__(self, broker: broker.Service, sender: sender.Service):
        self._broker = broker
        self._sender = sender

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._broker,
            self._sender,
        ]

    @property
    def broker(self) -> broker.Service:
        return self._broker

    @property
    def sender(self) -> sender.Service:
        return self._sender


def get_service(loop: asyncio.AbstractEventLoop, settings: Settings) -> Service:
    sender_service = sender.get_service(settings=settings.sender)
    broker_service = broker.get_service(loop=loop, sender=sender_service, settings=settings.broker)

    return Service(broker=broker_service, sender=sender_service)
