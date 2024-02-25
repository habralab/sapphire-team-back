from typing import Iterable

import socketio
import uvicorn
from facet import ServiceMixin
from loguru import logger

from sapphire.common.api.uvicorn_server import UvicornServer


class BaseWebSocketService(ServiceMixin):
    def __init__(
        self,
        title: str,
        root_path: str = '',
        allowed_origins: Iterable[str] = (),
        port: int = 8000,
    ):
        self._title = title
        self._root_path = root_path
        self._allowed_origins = allowed_origins
        self._port = port
        self._server = self._get_server()

    def _get_server(self) -> socketio.AsyncServer:
        sio_server = socketio.AsyncServer(
            async_mode='asgi',
            cors_allowed_origins=self._allowed_origins,
        )

        return sio_server

    def get_app(self) -> socketio.ASGIApp:
        sio_app = socketio.ASGIApp(
            socketio_server=self._server,
            socketio_path=self._root_path,
        )

        return sio_app

    async def start(self):
        config = uvicorn.Config(app=self.get_app(), host='0.0.0.0', port=self._port)
        server = UvicornServer(config)

        logger.info("Start Web Socket service {name}", name=self._title)
        self.add_task(server.serve())

    async def stop(self):
        logger.info("Stop Web Socket service {name}", name=self._title)

    @property
    def server(self):
        return self._server
