from pydantic import BaseModel

from .api import Settings as APISettings
from .database import Settings as DatabaseSettings


class Settings(BaseModel):
    api: APISettings = APISettings()
    database: DatabaseSettings = DatabaseSettings()
