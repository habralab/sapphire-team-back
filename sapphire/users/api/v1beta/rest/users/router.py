import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/{user_id}", methods=["POST"], endpoint=handlers.update_user)
