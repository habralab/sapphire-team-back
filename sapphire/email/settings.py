from pydantic import EmailStr, conint

from sapphire.common.broker.settings import BaseBrokerConsumerSettings


class EmailSettings(BaseBrokerConsumerSettings):
    consumer_servers: list[str] = ["localhost:9091"]
    topics: list[str] = ["email"]

    email_sender: EmailStr = "user@example.com"
    email_hostname: str = "smtp.gmail.com"
    email_port: conint(ge=1, le=65535) = 587
    email_start_tls: bool = False
    email_tls: bool = False


def get_settings() -> EmailSettings:
    return EmailSettings()
