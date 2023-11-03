import fastapi

from . import rest, websocket

router = fastapi.APIRouter()

router.include_router(rest.router, prefix="/rest")
router.include_router(websocket.router, prefix="/ws")
