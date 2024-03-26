import asyncio

from sapphire.common.broker.models.email import Email, EmailType
from sapphire.common.broker.service import BaseBrokerProducerService
from sapphire.database.models.users import User

from .settings import Settings


class Service(BaseBrokerProducerService):
    async def send_reset_password_email(self, user: User, code: str, topic: str = "email"):
        await self.send(
            topic=topic,
            message=Email(to=[user.email], type=EmailType.RESET_PASSWORD, data={"code": code}),
        )

    async def send_registration_email(self, user: User, topic: str = "email"):
        await self.send(
            topic=topic,
            message=Email(to=[user.email], type=EmailType.REGISTRATION),
        )


def get_service(
        loop: asyncio.AbstractEventLoop,
        settings: Settings,
) -> Service:
    return Service(loop=loop, servers=settings.servers)
