from pydantic_settings import SettingsConfigDict

from sapphire.common.api.settings import BaseAPISettings


class Settings(BaseAPISettings):
    model_config = SettingsConfigDict(env_file=".env", secrets_dir="/run/secrets", extra="allow")


def get_settings() -> Settings:
    return Settings()
