import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["GET"], endpoint=handlers.get_project_position_skills)
router.add_api_route(path="/", methods=["POST"], endpoint=handlers.update_project_position_skills)
