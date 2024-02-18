from pydantic import BaseModel

from sapphire.common.jwt.settings import JWTSettings
from .api import Settings as APISettings
from .broker import Settings as BrokerSettings
from .database import Settings as DatabaseSettings


class Settings(BaseModel):
    api: APISettings = APISettings()
    broker: BrokerSettings = BrokerSettings()
    database: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
