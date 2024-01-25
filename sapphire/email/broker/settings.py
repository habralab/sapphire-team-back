from sapphire.common.broker.settings import BaseBrokerConsumerSettings


class Settings(BaseBrokerConsumerSettings):
    consumer_servers: list[str] = ["localhost:9091"]
    topics: list[str] = ["email"]


def get_settings() -> Settings:
    return Settings()
