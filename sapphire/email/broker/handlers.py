import json
from typing import Iterable

import aiokafka

from sapphire.common.broker.handler import BaseBrokerHandler
from sapphire.common.broker.models.email import Email
from sapphire.email.sender.service import EmailSenderService


class EmailBrokerHandler(BaseBrokerHandler):
    def __init__(self, sender: EmailSenderService, topics: Iterable[str] | None = None):
        self._sender = sender

        super().__init__(topics=topics)

    def handle(self, message: aiokafka.ConsumerRecord):
        payload = json.loads(message.value)
        email = Email.model_validate(payload)

    @property
    def sender(self) -> EmailSenderService:
        return self._sender
