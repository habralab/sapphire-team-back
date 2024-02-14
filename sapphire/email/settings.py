from pydantic import BaseModel

from . import broker, sender


class Settings(BaseModel):
    broker: broker.Settings
    sender: sender.Settings
