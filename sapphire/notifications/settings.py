from pydantic import AnyUrl, conint
from pydantic_settings import BaseSettings, SettingsConfigDict


class NotificationsSettings(BaseSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    port: conint(ge=1, le=65535) = 8000
    root_path: str = ""
    allowed_origins: list[str] = []

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///notifications.sqlite3")


def get_settings() -> NotificationsSettings:
    return NotificationsSettings()
