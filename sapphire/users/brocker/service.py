import uuid

from sapphire.common.broker.models.email import Email
from sapphire.common.broker.service import BaseBrokerProducerService


class Service(BaseBrokerProducerService):

    async def _send_email(
            self, recipients: list[uuid.UUID], topic: str = "change_password"
    ):
        await self.send(topic=topic, message=Email(to=recipients))

    async def send_email_code(self, email: str, code: str):
        pass

# def get_service() -> Service:
#     return Service()
