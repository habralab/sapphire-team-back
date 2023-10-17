import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["POST"], endpoint=handlers.create_project_position)
router.add_api_route(path="/{position_id}", methods=["DELETE"],
                     endpoint=handlers.remove_project_position)
