import fastapi

from . import participants

router = fastapi.APIRouter()

router.include_router(participants.router, prefix="/{position_id}/participants")
