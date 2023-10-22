from facet import ServiceMixin

from .api.service import StorageAPIService
from .database.service import StorageDatabaseService


class StorageService(ServiceMixin):
    def __init__(self, api: StorageAPIService, database: StorageDatabaseService):
        self._api = api
        self._database = database

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
            self._database,
        ]


def get_service(api: StorageAPIService, database: StorageDatabaseService) -> StorageService:
    return StorageService(api=api, database=database)
