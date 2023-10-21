from pydantic import AnyHttpUrl

from sapphire.common.jwt.settings import JWTSettings


class AutotestsSettings(JWTSettings):
    messenger_base_url: AnyHttpUrl
    notifications_base_url: AnyHttpUrl
    projects_base_url: AnyHttpUrl
    storage_base_url: AnyHttpUrl
    users_base_url: AnyHttpUrl
