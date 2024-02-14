from pydantic import BaseModel


class BaseBrokerConsumerSettings(BaseModel):
    servers: list[str] = []
    topics: list[str] = []


class BaseBrokerProducerSettings(BaseModel):
    servers: list[str] = []
