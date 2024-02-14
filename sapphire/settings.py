from pydantic import BaseModel

from . import email, messenger, notifications, projects, storage, users


class Settings(BaseModel):
    email: email.Settings
    messenger: messenger.Settings
    notifications: notifications.Settings
    projects: projects.Settings
    storage: storage.Settings
    users: users.Settings
