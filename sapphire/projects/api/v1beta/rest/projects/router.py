import fastapi

from . import handlers, positions

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["POST"], endpoint=handlers.create_project)
router.add_api_route(path="/{project_id}", methods=["GET"], endpoint=handlers.get_project)
router.add_api_route(
    path="/{project_id}/history", methods=["GET"], endpoint=handlers.history
)
router.add_api_route(path="/", methods=["GET"], endpoint=handlers.get_projects)
router.include_router(positions.router, prefix="/{project_id}/positions")
