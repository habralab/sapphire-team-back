from pydantic import AnyUrl
from pydantic_settings import SettingsConfigDict

from sapphire.common.database.settings import BaseDatabaseSettings


class Settings(BaseDatabaseSettings):
    model_config = SettingsConfigDict(env_file=".env", secrets_dir="/run/secrets", extra="ignore")

    dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///projects.sqlite3")


def get_settings() -> Settings:
    return Settings()
