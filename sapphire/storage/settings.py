from pydantic import AnyHttpUrl, AnyUrl, conint
from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageSettings(BaseSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    port: conint(ge=1, le=65535) = 8000
    root_url: AnyHttpUrl = AnyHttpUrl("http://localhost:8000")
    root_path: str = ""
    allowed_origins: list[str] = []

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///storage.sqlite3")


def get_settings() -> StorageSettings:
    return StorageSettings()