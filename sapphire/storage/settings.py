from pydantic import AnyUrl
from pydantic_settings import SettingsConfigDict

from sapphire.common.api.settings import BaseAPISettings
from sapphire.common.database.settings import BaseDatabaseSettings
from sapphire.common.internal_api.settings import BaseInternalAPISettings


class StorageSettings(BaseAPISettings, BaseDatabaseSettings, BaseInternalAPISettings):
    model_config = SettingsConfigDict(secrets_dir="/run/secrets")

    db_dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///storage.sqlite3")


def get_settings() -> StorageSettings:
    return StorageSettings()
