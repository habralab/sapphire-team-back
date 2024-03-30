import asyncio

from facet import ServiceMixin

from collabry.common.habr import get_habr_client
from collabry.common.habr_career import get_habr_career_client
from collabry.common.jwt.methods import get_jwt_methods

from . import api, broker, cache, database, oauth2
from .settings import Settings


class Service(ServiceMixin):
    def __init__(self, api: api.Service):
        self._api = api

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
        ]

    @property
    def api(self) -> api.Service:
        return self._api


def get_service(loop: asyncio.AbstractEventLoop, settings: Settings) -> Service:
    broker_service = broker.get_service(loop=loop, settings=settings.broker)
    cache_service = cache.get_service(settings=settings.cache)
    database_service = database.get_service(settings=settings.database)
    oauth2_habr_service = oauth2.habr.get_service(settings=settings.oauth2_habr)
    habr_client = get_habr_client(settings=settings.habr)
    habr_career_client = get_habr_career_client(settings=settings.habr_career)
    jwt_methods = get_jwt_methods(settings=settings.jwt)
    api_service = api.get_service(
        broker=broker_service,
        cache=cache_service,
        database=database_service,
        oauth2_habr=oauth2_habr_service,
        habr_client=habr_client,
        habr_career_client=habr_career_client,
        jwt_methods=jwt_methods,
        settings=settings.api,
    )
    return Service(api=api_service)
