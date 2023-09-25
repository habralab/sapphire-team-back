import fastapi

from . import habr


router = fastapi.APIRouter()

router.include_router(habr.router, prefix="/habr")
