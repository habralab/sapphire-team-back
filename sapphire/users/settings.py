from pydantic import BaseModel

from sapphire.common.habr.settings import HabrSettings
from sapphire.common.habr_career.settings import HabrCareerSettings
from sapphire.common.jwt.settings import JWTSettings
from . import api, cache, database, oauth2


class Settings(BaseModel):
    api: api.Settings
    cache: cache.Settings
    database: database.Settings
    jwt: JWTSettings
    habr: HabrSettings
    habr_career: HabrCareerSettings
    oauth2_habr: oauth2.habr.Settings
