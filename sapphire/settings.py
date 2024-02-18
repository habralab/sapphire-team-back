from pydantic import BaseModel

from .email import Settings as EmailSettings
from .messenger import Settings as MessengerSettings
from .notifications import Settings as NotificationsSettings
from .projects import Settings as ProjectsSettings
from .storage import Settings as StorageSettings
from .users import Settings as UsersSettings


class Settings(BaseModel):
    email: EmailSettings = EmailSettings()
    messenger: MessengerSettings = MessengerSettings()
    notifications: NotificationsSettings = NotificationsSettings()
    projects: ProjectsSettings = ProjectsSettings()
    storage: StorageSettings = StorageSettings()
    users: UsersSettings = UsersSettings()
