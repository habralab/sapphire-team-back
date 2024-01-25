from sapphire.common.broker.settings import BaseBrokerConsumerSettings

from . import broker, sender


class Settings(BaseBrokerConsumerSettings):
    broker: broker.Settings
    sender: sender.Settings
    

def get_settings() -> Settings:
    return Settings()
