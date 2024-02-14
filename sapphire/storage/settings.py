from pydantic import BaseModel

from . import api, database


class Settings(BaseModel):
    api: api.Settings
    database: database.Settings
