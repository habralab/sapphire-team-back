from pydantic import AnyUrl, conint
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectsSettings(BaseSettings):
    model_config = SettingsConfigDict()

    port: conint(ge=1, le=65535) = 8000
    root_path: str = ""

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///projects.sqlite3")


def get_settings() -> ProjectsSettings:
    return ProjectsSettings()
