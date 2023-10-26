from queue import Queue

import websockets
from facet import ServiceMixin


class BaseWebsocketClient(ServiceMixin):
    def __init__(self, *urls: str):
        self._urls = urls
        self._connections = []
        self._queue = Queue()

    async def start(self):
        for url in self._urls:
            self._connections.append()
        self._connection = websockets.connect(self._url)
        await self._connection.__aenter__()

    async def stop(self):
        if self._connection is None:
            return

        await self._connection.__aexit__()
        self._connection = None

    async def listener(self):
        async for message in websockets.connect(self._url):
            message
