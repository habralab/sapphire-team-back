from pydantic_settings import SettingsConfigDict

from sapphire.common.broker.settings import BaseBrokerConsumerSettings


class Settings(BaseBrokerConsumerSettings):
    model_config = SettingsConfigDict(env_file=".env", secrets_dir="/run/secrets", extra="ignore")

    consumer_servers: list[str] = ["localhost:9091"]
    topics: list[str] = ["chats"]


def get_settings() -> Settings:
    return Settings()
