from sapphire.common.broker.settings import BaseBrokerConsumerSettings


class EmailSettings(BaseBrokerConsumerSettings):
    consumer_servers: list[str] = ["localhost:9091"]
    topics: list[str] = ["email"]


def get_settings() -> EmailSettings:
    return EmailSettings()
