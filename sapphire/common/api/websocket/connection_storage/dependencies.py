import fastapi

from sapphire.common.api.websocket.connection_storage.storage import WebsocketConnectionStorage
from sapphire.common.jwt.dependencies.websocket import is_auth
from sapphire.common.jwt.models import JWTData


async def store_connection(
        websocket: fastapi.WebSocket,
        jwt_data: JWTData = fastapi.Depends(is_auth),
):
    connection_storage: WebsocketConnectionStorage = (
        websocket.app.service.websocket_connection_storage
    )

    connection_storage.add(user_id=jwt_data.user_id, connection=websocket)
    yield connection_storage
    connection_storage.remove(user_id=jwt_data.user_id, connection=websocket)
