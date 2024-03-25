import asyncio
from sapphire.common.broker.models.email import Email, EmailType
from sapphire.common.broker.service import BaseBrokerProducerService

from . import Settings


class Service(BaseBrokerProducerService):
    async def send_email_code(self, email: str, code: str, topic: str = "email"):
        await self.send(
            topic=topic,
            message=Email(
                to=[email],
                type=EmailType.CHANGE_PASSWORD,
                sending_data=code
            )
        )


def get_service(
        loop: asyncio.AbstractEventLoop,
        settings: Settings,
) -> Service:
    return Service(loop=loop, servers=settings.servers)
