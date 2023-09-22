from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class UsersDatabaseSettings(BaseSettings):
    dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///users.sqlite3")


def get_settings() -> UsersDatabaseSettings:
    return UsersDatabaseSettings()
