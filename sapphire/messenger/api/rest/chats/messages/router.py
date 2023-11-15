import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["GET"], endpoint=handlers.get_messages)
router.add_api_route(path="/", methods=["POST"], endpoint=handlers.create_message)
