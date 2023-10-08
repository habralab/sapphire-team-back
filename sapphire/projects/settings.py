from pydantic import AnyHttpUrl, AnyUrl, conint
from pydantic_settings import SettingsConfigDict

from sapphire.common.api.jwt.settings import JWTSettings


class ProjectsSettings(JWTSettings):
    model_config = SettingsConfigDict()

    port: conint(ge=1, le=65535) = 8000
    root_url: AnyHttpUrl = AnyHttpUrl("http://localhost:8000")
    root_path: str = ""
    allowed_origins: list[str] = []

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///projects.sqlite3")


def get_settings() -> ProjectsSettings:
    return ProjectsSettings()
