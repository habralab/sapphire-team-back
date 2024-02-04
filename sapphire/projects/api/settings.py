import pathlib

from pydantic import PositiveInt
from pydantic_settings import SettingsConfigDict

from sapphire.common.api.settings import BaseAPISettings


class Settings(BaseAPISettings):
    model_config = SettingsConfigDict(env_file=".env", secrets_dir="/run/secrets", extra="ignore")

    media_dir_path: pathlib.Path = pathlib.Path("/media")
    load_file_chunk_size: PositiveInt = 1024 * 1024 # 1 Mb


def get_settings() -> Settings:
    return Settings()
