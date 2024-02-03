from pydantic_settings import BaseSettings

from . import email, messenger, notifications
from .projects.settings import ProjectsSettings
from .storage.settings import StorageSettings
from .users.settings import UsersSettings


class Settings(BaseSettings):
    email: email.Settings
    messenger: messenger.Settings
    notifications: notifications.Settings
    projects: ProjectsSettings
    storage: StorageSettings
    users: UsersSettings


def get_settings() -> Settings:
    return Settings()
