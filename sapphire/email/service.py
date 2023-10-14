from facet import ServiceMixin

from .broker.service import EmailBrokerService
from .sender.service import EmailSenderService


class EmailService(ServiceMixin):
    def __init__(self, broker: EmailBrokerService, sender: EmailSenderService):
        self._broker = broker
        self._sender = sender

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._broker,
            self._sender,
        ]

    @property
    def broker(self) -> EmailBrokerService:
        return self._broker

    @property
    def sender(self) -> EmailSenderService:
        return self._sender


def get_service(broker: EmailBrokerService, sender: EmailSenderService) -> EmailService:
    return EmailService(broker=broker, sender=sender)
