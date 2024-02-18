from pydantic import BaseModel

from .broker import Settings as BrokerSettings
from .sender import Settings as SenderSettings


class Settings(BaseModel):
    broker: BrokerSettings = BrokerSettings()
    sender: SenderSettings = SenderSettings()
