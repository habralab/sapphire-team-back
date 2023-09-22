from pydantic import conint
from pydantic_settings import BaseSettings

from .database.settings import UsersDatabaseSettings


class UsersSettings(BaseSettings):
    port: conint(ge=1, le=65535) = 8000

    database: UsersDatabaseSettings = UsersDatabaseSettings()


def get_settings() -> UsersSettings:
    return UsersSettings()
