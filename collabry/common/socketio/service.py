from typing import Iterable

import socketio
import uvicorn
from facet import ServiceMixin
from loguru import logger

from collabry.common.uvicorn_server import UvicornServer


class BaseSocketIOService(ServiceMixin):
    def __init__(
        self,
        root_path: str = "",
        allowed_origins: Iterable[str] = (),
        port: int = 8000,
        namespaces: dict[str, socketio.AsyncNamespace] | None = None,
    ):
        self._root_path = root_path
        self._port = port
        self._server = socketio.AsyncServer(
            async_mode="asgi",
            cors_allowed_origins=allowed_origins,
        )
        for name, namespace in (namespaces or {}).items():
            self._server.register_namespace(namespace(name))

    def get_app(self) -> socketio.ASGIApp:
        sio_app = socketio.ASGIApp(
            socketio_server=self._server,
            socketio_path=self._root_path,
        )
        return sio_app

    async def start(self):
        config = uvicorn.Config(app=self.get_app(), host="0.0.0.0", port=self._port)
        server = UvicornServer(config)

        logger.info("Start Socket IO service")
        self.add_task(server.serve())

    async def stop(self):
        logger.info("Stop Socket IO service")
