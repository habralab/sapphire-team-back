from pydantic import BaseModel

from sapphire.common.jwt.settings import JWTSettings
from . import api, broker, database


class Settings(BaseModel):
    api: api.Settings
    broker: broker.Settings
    database: database.Settings
    jwt: JWTSettings
