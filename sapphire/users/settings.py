from typing import Iterable
import datetime

from pydantic import AnyUrl, conint
from pydantic_settings import BaseSettings, SettingsConfigDict


class UsersSettings(BaseSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    port: conint(ge=1, le=65535) = 8000
    root_path: str = ""
    allowed_origins: list[str] = []

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///users.sqlite3")

    habr_oauth2_client_id: str = ""
    habr_oauth2_client_secret: str = ""
    jwt_access_token_private_key: str
    jwt_access_token_public_key: str
    jwt_refresh_token_private_key: str
    jwt_refresh_token_public_key: str
    jwt_access_token_expires: datetime.timedelta = datetime.timedelta(minutes=5)
    jwt_refresh_token_expires: datetime.timedelta = datetime.timedelta(days=30)


def get_settings() -> UsersSettings:
    return UsersSettings()
