from facet import ServiceMixin

from .api.service import StorageAPIService
from .database.service import StorageDatabaseService
from .internal_api.service import StorageInternalAPIService


class StorageService(ServiceMixin):
    def __init__(
            self,
            api: StorageAPIService,
            internal_api: StorageInternalAPIService,
            database: StorageDatabaseService,
    ):
        self._api = api
        self._internal_api = internal_api
        self._database = database

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._api,
            self._internal_api,
            self._database,
        ]


def get_service(
        api: StorageAPIService,
    internal_api: StorageInternalAPIService,
        database: StorageDatabaseService,
) -> StorageService:
    return StorageService(api=api, internal_api=internal_api, database=database)
