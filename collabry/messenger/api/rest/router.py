import fastapi

from . import chats

router = fastapi.APIRouter()

router.include_router(chats.router, prefix="/chats")
