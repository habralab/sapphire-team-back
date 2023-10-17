import fastapi

from . import handlers, participants

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["POST"], endpoint=handlers.create_project_position)
router.include_router(participants.router, prefix="/{position_id}/participants")
