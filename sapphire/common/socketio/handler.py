from typing import Callable


class BaseSocketIOHandler:
    def __init__(self, event: str, handle: Callable):
        self._event = event
        self._handle = handle

    @property
    def event(self):
        return self._event

    @property
    def handle(self):
        return self._handle 
