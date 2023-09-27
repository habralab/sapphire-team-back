from enum import Enum


class ResponseStatus(Enum):
    OK = "ok"
    ERROR = "error"


class ServiceName(Enum):
    EMAIL = "email"
    MESSENGER = "messenger"
    NOTIFICATIONS = "notifications"
    PROJECTS = "projects"
    STORAGE = "storage"
    USERS = "users"
