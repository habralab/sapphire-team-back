import asyncio
import uuid
from typing import Any, Iterable

import aiosmtplib
import backoff
from facet import ServiceMixin

from sapphire.email.settings import EmailSettings

from .templates import Template


class EmailSenderService(ServiceMixin):
    TEMPLATES = ()

    def __init__(
            self,
            sender: str = "user@example.com",
            hostname: str = "smtp.gmail.com",
            port: int = 587,
            start_tls: bool = False,
            tls: bool = False,
    ):
        self._sender = sender
        self._client = aiosmtplib.SMTP(
            hostname=hostname,
            port=port,
            start_tls=start_tls,
            use_tls=tls,
        )

        self._templates = {template.name: template for template in self.TEMPLATES}

    @property
    def templates(self) -> dict[str, Template]:
        return self._templates

    async def _get_recipient_email(self, recipient: uuid.UUID) -> str:
        # Issue: Write a function to get email from the users service using user_id

        return "email@example.com"

    async def send(self, template: Template, data: dict[str, Any], recipients: Iterable[uuid.UUID]):
        coroutines = []
        for recipient in recipients:
            recipient_email = await self._get_recipient_email(recipient)
            message = template.render(recipient=recipient_email, sender=self._sender, data=data)
            coroutine = backoff.on_exception(backoff.expo, Exception, max_tries=3)(
                self._client.send_message,
            )(message)
            coroutines.append(coroutine)

        async with self._client:
            await asyncio.gather(*coroutines)


def get_service(settings: EmailSettings) -> EmailSenderService:
    return EmailSenderService(
        sender=settings.email_sender,
        hostname=settings.email_hostname,
        port=settings.email_port,
        start_tls=settings.email_start_tls,
        tls=settings.email_tls,
    )
