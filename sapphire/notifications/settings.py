from pydantic import AnyUrl
from pydantic_settings import SettingsConfigDict

from sapphire.common.api.settings import BaseAPISettings
from sapphire.common.database.settings import BaseDatabaseSettings


class NotificationsSettings(BaseAPISettings, BaseDatabaseSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///notifications.sqlite3")


def get_settings() -> NotificationsSettings:
    return NotificationsSettings()
