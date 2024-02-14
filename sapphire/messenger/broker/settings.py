from sapphire.common.broker.settings import BaseBrokerConsumerSettings


class Settings(BaseBrokerConsumerSettings):
    servers: list[str] = ["localhost:9091"]
    topics: list[str] = ["chats"]
