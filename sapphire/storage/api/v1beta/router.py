import fastapi

from . import specialization

router = fastapi.APIRouter()

router.include_router(specialization.router, prefix="/specializations")
