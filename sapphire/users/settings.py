import pathlib

from pydantic import AnyUrl, PositiveInt
from pydantic_settings import SettingsConfigDict

from sapphire.common.api.settings import BaseAPISettings
from sapphire.common.database.settings import BaseDatabaseSettings
from sapphire.common.habr.settings import HabrSettings
from sapphire.common.jwt.settings import JWTSettings
from sapphire.common.utils.rsa256 import generate_rsa_keys

access_token = generate_rsa_keys()
refresh_token = generate_rsa_keys()


class UsersSettings(BaseAPISettings, BaseDatabaseSettings, JWTSettings, HabrSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///users.sqlite3")

    habr_oauth2_client_id: str = ""
    habr_oauth2_client_secret: str = ""

    media_dir_path: pathlib.Path = pathlib.Path("/media")
    load_file_chunk_size: PositiveInt = 1024 * 1024 # 1 Mb


def get_settings() -> UsersSettings:
    return UsersSettings()
