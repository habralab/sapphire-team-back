import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/{user_id}", methods=["GET"], endpoint=handlers.get_user)
router.add_api_route(path="/{user_id}", methods=["POST"], endpoint=handlers.update_user)
router.add_api_route(path="/{user_id}/avatar", methods=["GET"], endpoint=handlers.get_user_avatar)
router.add_api_route(path="/{user_id}/avatar", methods=["POST"],
                     endpoint=handlers.upload_user_avatar)
