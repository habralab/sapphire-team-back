import asyncio

from pydantic import EmailStr

from sapphire.common.broker.models.email import Email, EmailType
from sapphire.common.broker.service import BaseBrokerProducerService

from . import Settings


class Service(BaseBrokerProducerService):
    async def send_email_code(self, email: EmailStr, code: str, topic: str = "email"):
        await self.send(
            topic=topic,
            message=Email(
                to=[email],
                type=EmailType.RESET_PASSWORD,
                sending_data={"code": code}
            )
        )


def get_service(
        loop: asyncio.AbstractEventLoop,
        settings: Settings,
) -> Service:
    return Service(loop=loop, servers=settings.servers)
