from pydantic import AnyUrl, conint
from pydantic_settings import BaseSettings, SettingsConfigDict


class UsersSettings(BaseSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    port: conint(ge=1, le=65535) = 8000
    root_path: str = ""

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///users.sqlite3")

    habr_oauth2_client_id: str
    habr_oauth2_client_secret: str


def get_settings() -> UsersSettings:
    return UsersSettings()
