import fastapi

from . import websocket

router = fastapi.APIRouter()
router.include_router(websocket.router, prefix="/websocket")
