from pydantic_settings import BaseSettings


class BaseBrokerConsumerSettings(BaseSettings):
    consumer_servers: list[str] = []
    topics: list[str] = []


class BaseBrokerProducerSettings(BaseSettings):
    producer_servers: list[str] = []
