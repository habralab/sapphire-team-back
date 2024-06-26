from typing import Iterable

import aiokafka
from loguru import logger

from collabry.common.broker.handler import BaseBrokerHandler
from collabry.common.broker.models.email import Email
from collabry.email.sender import Service as SenderService


class SendEmailHandler(BaseBrokerHandler):
    def __init__(self, sender: SenderService, topics: Iterable[str] | None = None):
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
    def sender(self) -> SenderService:
        return self._sender
