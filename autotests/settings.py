from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class AutotestsSettings(BaseSettings):
    messenger_base_url: AnyHttpUrl
    notifications_base_url: AnyHttpUrl
    projects_base_url: AnyHttpUrl
    storage_base_url: AnyHttpUrl
    users_base_url: AnyHttpUrl
