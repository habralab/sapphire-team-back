import fastapi

from . import handlers, messages

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["GET"], endpoint=handlers.get_chats)
router.add_api_route(path="/{chat_id}", methods=["GET"], endpoint=handlers.get_chat)
router.include_router(messages.router, prefix="/{chat_id}/messages")
