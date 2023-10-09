from pydantic import AnyUrl
from pydantic_settings import SettingsConfigDict

from sapphire.common.api.jwt.settings import JWTSettings
from sapphire.common.api.settings import BaseAPISettings
from sapphire.common.database.settings import BaseDatabaseSettings
from sapphire.common.utils.rsa256 import generate_rsa_keys

access_token = generate_rsa_keys()
refresh_token = generate_rsa_keys()


class UsersSettings(BaseAPISettings, BaseDatabaseSettings, JWTSettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///users.sqlite3")

    habr_oauth2_client_id: str = ""
    habr_oauth2_client_secret: str = ""


def get_settings() -> UsersSettings:
    return UsersSettings()
