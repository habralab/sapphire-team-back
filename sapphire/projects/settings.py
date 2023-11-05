import pathlib

from pydantic import AnyUrl
from pydantic_settings import SettingsConfigDict

from sapphire.common.api.settings import BaseAPISettings
from sapphire.common.broker.settings import BaseBrokerProducerSettings
from sapphire.common.database.settings import BaseDatabaseSettings
from sapphire.common.jwt.settings import JWTSettings


class ProjectsSettings(BaseAPISettings, BaseBrokerProducerSettings, BaseDatabaseSettings,
                       JWTSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///projects.sqlite3")

    media_dir_path: pathlib.Path = pathlib.Path("/media")

    producer_servers: list[str] = ["localhost:9091"]

    topics = list[str] = ["chats"]


def get_settings() -> ProjectsSettings:
    return ProjectsSettings()
