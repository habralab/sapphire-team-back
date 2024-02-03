from pydantic_settings import SettingsConfigDict

from sapphire.common.broker.settings import BaseBrokerConsumerSettings

from . import broker, sender


class Settings(BaseBrokerConsumerSettings):
    model_config = SettingsConfigDict(env_file=".env", secrets_dir="/run/secrets", extra="ignore")

    broker: broker.Settings
    sender: sender.Settings


def get_settings() -> Settings:
    return Settings()
