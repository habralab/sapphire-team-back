from typing import Iterable

import fastapi
from facet import ServiceMixin

from sapphire.common.api.service import BaseAPIService
from sapphire.common.api.websocket.connection_storage.storage import WebsocketConnectionStorage
from sapphire.common.jwt import JWTMethods
from sapphire.common.utils.package import get_version
from sapphire.notifications.database.service import NotificationsDatabaseService
from sapphire.notifications.settings import NotificationsSettings

from . import health, router


class NotificationsAPIService(BaseAPIService):
    def __init__(
        self,
        database: NotificationsDatabaseService,
        jwt_methods: JWTMethods,
        websocket_connection_storage: WebsocketConnectionStorage,
        version: str = "0.0.0",
        root_url: str = "http://localhost",
        root_path: str = "",
        allowed_origins: Iterable[str] = (),
        port: int = 8000,
    ):
        self._database = database
        self._jwt_methods = jwt_methods
        self._websocket_connection_storage = websocket_connection_storage

        super().__init__(
            title="Notifications",
            version=version,
            root_url=root_url,
            root_path=root_path,
            allowed_origins=allowed_origins,
            port=port,
        )

    def setup_app(self, app: fastapi.FastAPI):
        app.add_api_route(path="/health", endpoint=health.health)
        app.include_router(router.router, prefix="/api")

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._database,
        ]

    @property
    def database(self) -> NotificationsDatabaseService:
        return self._database

    @property
    def jwt_methods(self) -> JWTMethods:
        return self._jwt_methods

    @property
    def websocket_connection_storage(self) -> WebsocketConnectionStorage:
        return self._websocket_connection_storage


def get_service(
    database: NotificationsDatabaseService,
    jwt_methods: JWTMethods,
    websocket_connection_storage: WebsocketConnectionStorage,
    settings: NotificationsSettings,
) -> NotificationsAPIService:
    return NotificationsAPIService(
        database=database,
        jwt_methods=jwt_methods,
        websocket_connection_storage=websocket_connection_storage,
        version=get_version() or "0.0.0",
        root_url=str(settings.root_url),
        root_path=settings.root_path,
        allowed_origins=settings.allowed_origins,
        port=settings.port,
    )
