from typing import Iterable

import fastapi
from facet import ServiceMixin

from sapphire.common.api.service import BaseAPIService
from sapphire.common.utils.package import get_version
from sapphire.storage.api.router import router
from sapphire.storage.database.service import StorageDatabaseService
from sapphire.storage.settings import StorageSettings


class StorageAPIService(BaseAPIService):
    def __init__(
        self,
        database: StorageDatabaseService,
        version: str = "0.0.0",
        root_url: str = "http://localhost",
        root_path: str = "",
        allowed_origins: Iterable[str] = (),
        port: int = 8000,
    ):
        self._database = database

        super().__init__(
            title="Storage",
            version=version,
            root_url=root_url,
            root_path=root_path,
            allowed_origins=allowed_origins,
            port=port,
        )

    def setup_app(self, app: fastapi.FastAPI):
        app.include_router(router, prefix="/api")

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._database,
        ]

    @property
    def database(self) -> StorageDatabaseService:
        return self._database


def get_service(
    database: StorageDatabaseService,
    settings: StorageSettings,
) -> StorageAPIService:
    return StorageAPIService(
        database=database,
        version=get_version() or "0.0.0",
        root_url=str(settings.root_url),
        root_path=settings.root_path,
        allowed_origins=settings.allowed_origins,
        port=settings.port,
    )
