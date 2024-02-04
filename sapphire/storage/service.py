from facet import ServiceMixin

from . import api, database
from .settings import Settings


class Service(ServiceMixin):
    def __init__(self, api: api.Service, database: database.Service):
        self._api = api
        self._database = database

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
            self._database,
        ]


def get_service(settings: Settings) -> Service:
    database_service = database.get_service(settings=settings.database)
    api_service = api.get_service(database=database_service, settings=settings.api)
    return Service(api=api_service, database=database_service)
