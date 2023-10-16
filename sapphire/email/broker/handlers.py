from typing import Iterable

import aiokafka
from loguru import logger

from sapphire.common.broker.handler import BaseBrokerHandler
from sapphire.common.broker.models.email import Email
from sapphire.email.sender.service import EmailSenderService


class EmailBrokerHandler(BaseBrokerHandler):
    def __init__(self, sender: EmailSenderService, topics: Iterable[str] | None = None):
        self._sender = sender

        super().__init__(topics=topics)

    async def handle(self, message: aiokafka.ConsumerRecord):
        email = Email.model_validate_json(json_data=message.value)
        template = self._sender.templates.get(email.type)
        if template is None:
            logger.error("Template '{}' is not exist", email.type)
            return

        await self._sender.send(template=template, data=email.data, recipients=email.to)

    @property
    def sender(self) -> EmailSenderService:
        return self._sender
