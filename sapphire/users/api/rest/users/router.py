import fastapi

from sapphire.common.api.openapi import IMAGE_SCHEMA

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/{user_id}", methods=["GET"], endpoint=handlers.get_user)
router.add_api_route(path="/{user_id}", methods=["POST"], endpoint=handlers.update_user)
router.add_api_route(path="/{user_id}/avatar", methods=["GET"], endpoint=handlers.get_user_avatar,
                     responses={fastapi.status.HTTP_200_OK: IMAGE_SCHEMA})
router.add_api_route(path="/{user_id}/avatar", methods=["POST"],
                     endpoint=handlers.upload_user_avatar)
router.add_api_route(path="/{user_id}/avatar", methods=["DELETE"],
                     endpoint=handlers.delete_user_avatar)
router.add_api_route(path="/{user_id}/skills", methods=["GET"],
                     endpoint=handlers.get_user_skills)
router.add_api_route(path="/{user_id}/skills", methods=["POST"],
                     endpoint=handlers.update_user_skills)
