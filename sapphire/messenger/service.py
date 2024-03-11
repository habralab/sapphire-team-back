from asyncio import AbstractEventLoop

from facet import ServiceMixin

from sapphire.common.jwt.methods import get_jwt_methods

from . import api, broker, database
from .settings import Settings


class Service(ServiceMixin):
    def __init__(self, api: api.Service, broker: broker.Service):
        self._api = api
        self._broker = broker

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
            self._broker,
        ]

    @property
    def api(self) -> api.Service:
        return self._api

    @property
    def broker(self) -> broker.Service:
        return self._broker


def get_service(loop: AbstractEventLoop, settings: Settings) -> Service:
    jwt_methods = get_jwt_methods(settings=settings.jwt)
    database_service = database.get_service(settings=settings.database)
    api_service = api.get_service(
        database=database_service,
        jwt_methods=jwt_methods,
        settings=settings.api,
    )
    broker_service = broker.get_service(
        loop=loop,
        database=database_service,
        settings=settings.broker,
    )
    return Service(api=api_service, broker=broker_service)
