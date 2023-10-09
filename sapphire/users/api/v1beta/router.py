import fastapi

from . import rest

router = fastapi.APIRouter()

router.include_router(rest.router, prefix="/rest")
