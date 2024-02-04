from pydantic_settings import BaseSettings

from . import email, messenger, notifications, projects
from .storage.settings import StorageSettings
from .users.settings import UsersSettings


class Settings(BaseSettings):
    email: email.Settings
    messenger: messenger.Settings
    notifications: notifications.Settings
    projects: projects.Settings
    storage: StorageSettings
    users: UsersSettings


def get_settings() -> Settings:
    return Settings()
