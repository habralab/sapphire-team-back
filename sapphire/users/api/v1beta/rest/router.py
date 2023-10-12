import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/users", methods=["POST"], endpoint=handlers.update)
