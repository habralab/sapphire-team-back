from pydantic import AnyHttpUrl
from pydantic_settings import SettingsConfigDict

from sapphire.common.jwt.settings import JWTSettings


class AutotestsSettings(JWTSettings):
    model_config = SettingsConfigDict(extra="allow", env_file=".env")

    messenger_base_url: AnyHttpUrl
    notifications_base_url: AnyHttpUrl
    projects_base_url: AnyHttpUrl
    storage_base_url: AnyHttpUrl
    users_base_url: AnyHttpUrl
