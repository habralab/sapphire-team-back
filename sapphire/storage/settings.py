from pydantic_settings import BaseSettings, SettingsConfigDict

from . import api, database


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", secrets_dir="/run/secrets", extra="ignore")

    api: api.Settings
    database: database.Settings


def get_settings() -> Settings:
    return Settings()
