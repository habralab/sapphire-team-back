from pydantic import AnyUrl
from pydantic_settings import SettingsConfigDict

from sapphire.common.api.jwt.settings import JWTSettings
from sapphire.common.api.settings import BaseAPISettings
from sapphire.common.database.settings import BaseDatabaseSettings


class ProjectsSettings(BaseAPISettings, BaseDatabaseSettings, JWTSettings):
    model_config = SettingsConfigDict()

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///projects.sqlite3")


def get_settings() -> ProjectsSettings:
    return ProjectsSettings()
