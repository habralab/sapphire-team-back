from sapphire.common.broker.settings import BaseBrokerConsumerSettings


class EmailSettings(BaseBrokerConsumerSettings):
    pass


def get_settings() -> EmailSettings:
    return EmailSettings()
