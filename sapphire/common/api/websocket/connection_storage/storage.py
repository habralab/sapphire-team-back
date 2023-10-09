import uuid
from collections import defaultdict

import fastapi


class WebsocketConnectionStorage:
    def __init__(self):
        self._storage = defaultdict(dict)

    def add(self, user_id: uuid.UUID, connection: fastapi.WebSocket):
        self._storage[user_id][id(connection)] = connection

    def remove(self, user_id: uuid.UUID, connection: fastapi.WebSocket | None = None):
        if user_id not in self._storage:
            return

        if connection is None:
            del self._storage[user_id]
        else:
            self._storage[user_id].pop(id(connection), None)

    def get_connections(self, user_id: uuid.UUID) -> tuple[fastapi.WebSocket]:
        return tuple(self._storage[user_id].values())


def get_storage() -> WebsocketConnectionStorage:
    return WebsocketConnectionStorage()
