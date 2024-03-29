import asyncio

from facet import ServiceMixin

from . import email, messenger, notifications, projects, storage, users
from .settings import Settings


class Service(ServiceMixin):
    def __init__(
            self,
            email: email.Service,
            messenger: messenger.Service,
            notifications: notifications.Service,
            projects: projects.Service,
            storage: storage.Service,
            users: users.Service,
    ):
        self._email = email
        self._messenger = messenger
        self._notifications = notifications
        self._projects = projects
        self._storage = storage
        self._users = users

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._email,
            self._messenger,
            self._notifications,
            self._projects,
            self._storage,
            self._users,
        ]

    @property
    def email(self) -> email.Service:
        return self._email

    @property
    def messenger(self) -> messenger.Service:
        return self._messenger

    @property
    def notifications(self) -> notifications.Service:
        return self._notifications

    @property
    def projects(self) -> projects.Service:
        return self._projects

    @property
    def storage(self) -> storage.Service:
        return self._storage

    @property
    def users(self) -> users.Service:
        return self._users


def get_service(loop: asyncio.AbstractEventLoop, settings: Settings) -> Service:
    email_service = email.get_service(loop=loop, settings=settings.email)
    messenger_service = messenger.get_service(loop=loop, settings=settings.messenger)
    notifications_service = notifications.get_service(loop=loop, settings=settings.notifications)
    projects_service = projects.get_service(loop=loop, settings=settings.projects)
    storage_service = storage.get_service(settings=settings.storage)
    users_service = users.get_service(loop=loop, settings=settings.users)

    return Service(
        email=email_service,
        messenger=messenger_service,
        notifications=notifications_service,
        projects=projects_service,
        storage=storage_service,
        users=users_service,
    )
