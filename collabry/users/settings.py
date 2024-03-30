from pydantic import BaseModel

from collabry.common.habr.settings import HabrSettings
from collabry.common.habr_career.settings import HabrCareerSettings
from collabry.common.jwt.settings import JWTSettings

from .api import Settings as APISettings
from .broker import Settings as BrokerSettings
from .cache import Settings as CacheSettings
from .database import Settings as DatabaseSettings
from .oauth2.habr import Settings as OAuth2HabrSettings


class Settings(BaseModel):
    api: APISettings = APISettings()
    cache: CacheSettings = CacheSettings()
    database: DatabaseSettings = DatabaseSettings()
    jwt: JWTSettings = JWTSettings()
    habr: HabrSettings = HabrSettings()
    habr_career: HabrCareerSettings = HabrCareerSettings()
    oauth2_habr: OAuth2HabrSettings = OAuth2HabrSettings()
    broker: BrokerSettings = BrokerSettings()
