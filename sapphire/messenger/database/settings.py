from pydantic import AnyUrl
from pydantic_settings import SettingsConfigDict

from sapphire.common.database.settings import BaseDatabaseSettings


class Settings(BaseDatabaseSettings):
    model_config = SettingsConfigDict(env_file=".env", secrets_dir="/run/secrets", extra="allow")

    dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///messenger.sqlite3")


def get_settings() -> Settings:
    return Settings()
