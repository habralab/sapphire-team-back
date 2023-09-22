from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    dsn: AnyUrl


def get_settings(dsn: str) -> DatabaseSettings:
    return DatabaseSettings(dsn=AnyUrl(dsn))
