import fastapi

from sapphire.common.api.websocket.connection_storage.dependencies import store_connection
from sapphire.common.api.websocket.connection_storage.storage import WebsocketConnectionStorage


async def notifications(
        websocket: fastapi.WebSocket,
        connection_storage: WebsocketConnectionStorage = fastapi.Depends(store_connection),
):
    await websocket.accept()
    while True:
        await websocket.receive_json()
