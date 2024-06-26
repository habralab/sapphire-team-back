import fastapi

from collabry.common.api.openapi import IMAGE_SCHEMA

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["GET"], endpoint=handlers.get_projects)
router.add_api_route(path="/", methods=["POST"], endpoint=handlers.create_project)
router.add_api_route(path="/{project_id}", methods=["GET"], endpoint=handlers.get_project)
router.add_api_route(path="/{project_id}", methods=["PATCH"],
                     endpoint=handlers.partial_update_project)
router.add_api_route(path="/{project_id}/avatar", methods=["GET"],
                     endpoint=handlers.get_project_avatar, responses={
                         fastapi.status.HTTP_200_OK: IMAGE_SCHEMA,
                     })
router.add_api_route(path="/{project_id}/avatar", methods=["POST"],
                     endpoint=handlers.upload_project_avatar)
router.add_api_route(path="/{project_id}/avatar", methods=["DELETE"],
                     endpoint=handlers.delete_project_avatar)
router.add_api_route(path="/{project_id}/history", methods=["GET"], endpoint=handlers.history)
