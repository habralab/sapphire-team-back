import asyncio
from typing import Any, Iterable

import aiosmtplib
import backoff
from facet import ServiceMixin
from pydantic import EmailStr

from .settings import Settings
from .templates import Template


class Service(ServiceMixin):
    TEMPLATES = (
        Template.load("registration"),
    )

    def __init__(
            self,
            username: str = "user@example.com",
            password: str = "P@ssw0rd",
            host: str = "smtp.gmail.com",
            port: int = 587,
            start_tls: bool = False,
            tls: bool = False,
    ):
        self._username = username
        self._client = aiosmtplib.SMTP(
            hostname=host,
            port=port,
            username=username,
            password=password,
            start_tls=start_tls,
            use_tls=tls,
        )

        self._templates = {template.name: template for template in self.TEMPLATES}

    @property
    def templates(self) -> dict[str, Template]:
        return self._templates

    async def send(self, template: Template, data: dict[str, Any], recipients: Iterable[EmailStr]):
        coroutines = []
        for recipient in recipients:
            message = template.render(recipient=recipient, sender=self._username, data=data)
            coroutine = backoff.on_exception(backoff.expo, Exception, max_tries=3)(
                self._client.send_message,
            )(message)
            coroutines.append(coroutine)

        async with self._client:
            await asyncio.gather(*coroutines)


def get_service(settings: Settings) -> Service:
    return Service(
        username=settings.username,
        password=settings.password,
        host=settings.host,
        port=settings.port,
        start_tls=settings.start_tls,
        tls=settings.tls,
    )
