from pydantic_settings import BaseSettings, SettingsConfigDict

from sapphire.common.jwt.settings import JWTSettings
from . import api, broker, database


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", secrets_dir="/run/secrets", extra="ignore")

    api: api.Settings
    broker: broker.Settings
    database: database.Settings
    jwt: JWTSettings


def get_settings() -> Settings:
    return Settings()
