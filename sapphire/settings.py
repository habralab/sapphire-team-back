from pydantic_settings import BaseSettings

from . import email
from .messenger.settings import MessengerSettings
from .notifications.settings import NotificationsSettings
from .projects.settings import ProjectsSettings
from .storage.settings import StorageSettings
from .users.settings import UsersSettings


class Settings(BaseSettings):
    email: email.Settings
    messenger: MessengerSettings
    notifications: NotificationsSettings
    projects: ProjectsSettings
    storage: StorageSettings
    users: UsersSettings


def get_settings() -> Settings:
    return Settings()
