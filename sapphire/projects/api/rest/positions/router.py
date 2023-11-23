import fastapi

from . import handlers, skills

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["GET"], endpoint=handlers.get_positions)
router.add_api_route(path="/", methods=["POST"], endpoint=handlers.create_position)
router.add_api_route(path="/{position_id}", methods=["GET"], endpoint=handlers.get_position)
router.add_api_route(path="/{position_id}", methods=["DELETE"], endpoint=handlers.remove_position)
router.include_router(skills.router, prefix="/{position_id}/skills")
