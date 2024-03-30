from collabry.common.broker.settings import BaseBrokerProducerSettings


class Settings(BaseBrokerProducerSettings):
    servers: list[str] = ["localhost:9091"]
