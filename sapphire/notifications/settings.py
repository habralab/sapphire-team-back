from pydantic import AnyUrl
from pydantic_settings import SettingsConfigDict

from sapphire.common.api.settings import BaseAPISettings
from sapphire.common.broker.settings import BaseBrokerConsumerSettings
from sapphire.common.database.settings import BaseDatabaseSettings
from sapphire.common.jwt.settings import JWTSettings


class NotificationsSettings(BaseAPISettings, BaseBrokerConsumerSettings, BaseDatabaseSettings,
                            JWTSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///notifications.sqlite3")

    consumer_servers: list[str] = ["localhost:9091"]
    topics: list[str] = ["notifications"]


def get_settings() -> NotificationsSettings:
    return NotificationsSettings()
