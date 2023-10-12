import uuid

import fastapi

from sapphire.common.api.websocket.connection_storage.storage import WebsocketConnectionStorage
from sapphire.common.jwt.dependencies.websocket import get_user_id


async def store_connection(
        websocket: fastapi.WebSocket,
        user_id: uuid.UUID = fastapi.Depends(get_user_id),
):
    connection_storage: WebsocketConnectionStorage = (
        websocket.app.service.websocket_connection_storage
    )

    connection_storage.add(user_id=user_id, connection=websocket)
    yield connection_storage
    connection_storage.remove(user_id=user_id, connection=websocket)
