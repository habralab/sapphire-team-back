import fastapi

from . import handlers, positions

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["POST"], endpoint=handlers.create_project)
router.include_router(positions.router, prefix="/{project_id}/positions")
