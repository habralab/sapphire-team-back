import pathlib

from pydantic import AnyUrl, PositiveInt
from pydantic_settings import SettingsConfigDict

from sapphire.common.api.settings import BaseAPISettings
from sapphire.common.broker.settings import BaseBrokerProducerSettings
from sapphire.common.database.settings import BaseDatabaseSettings
from sapphire.common.jwt.settings import JWTSettings
from sapphire.users.internal_api.client.settings import UsersInternalAPIClientSettings


class ProjectsSettings(BaseAPISettings, BaseBrokerProducerSettings, BaseDatabaseSettings,
                       JWTSettings, UsersInternalAPIClientSettings):
    model_config = SettingsConfigDict(env_file=".env", secrets_dir="/run/secrets", extra="allow")

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///projects.sqlite3")

    media_dir_path: pathlib.Path = pathlib.Path("/media")
    load_file_chunk_size: PositiveInt = 1024 * 1024 # 1 Mb

    producer_servers: list[str] = ["localhost:9091"]


def get_settings() -> ProjectsSettings:
    return ProjectsSettings()
