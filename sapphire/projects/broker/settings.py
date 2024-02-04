from sapphire.common.broker.settings import BaseBrokerProducerSettings


class Settings(BaseBrokerProducerSettings):
    producer_servers: list[str] = ["localhost:9091"]


def get_settings() -> Settings:
    return Settings()
