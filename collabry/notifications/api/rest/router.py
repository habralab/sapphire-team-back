import fastapi

from . import notifications

router = fastapi.APIRouter()

router.include_router(notifications.router, prefix="/notifications")
