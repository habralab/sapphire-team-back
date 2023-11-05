from pydantic import AnyUrl
from pydantic_settings import SettingsConfigDict

from sapphire.common.api.settings import BaseAPISettings
from sapphire.common.database.settings import BaseDatabaseSettings
from sapphire.common.jwt.settings import JWTSettings


class MessengerSettings(BaseAPISettings, BaseDatabaseSettings, JWTSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///messenger.sqlite3")

    consumer_servers: list[str] = ["localhost:9091"]

    topics: list[str] = ["chats"]


def get_settings() -> MessengerSettings:
    return MessengerSettings()
