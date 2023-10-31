from queue import Empty, Queue
from typing import Any

import websockets
from facet import ServiceMixin


class WebsocketClient(ServiceMixin):
    def __init__(self, *urls: str, headers: dict[str, Any] | None = None, verify: bool = True):
        self._urls = urls
        self._headers = headers or {}
        self._verify = verify
        self._queue = Queue()

    async def start(self):
        for url in self._urls:
            self.add_task(self.listener(url))

    async def listener(self, url: str):
        for websocket in websockets.connect(url, extra_headers=self._headers, ssl=self._verify):
            try:
                message = await websocket.recv()
            except websockets.ConnectionClosed:
                continue

            self._queue.put(message)

    def get(self, timeout: float | None = None) -> str | None:
        try:
            return self._queue.get(timeout=timeout)
        except Empty:
            return None
