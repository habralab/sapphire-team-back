import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/", endpoint=handlers.update_project_position_skills)
