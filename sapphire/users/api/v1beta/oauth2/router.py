import fastapi

from . import habr, jwt_auth

router = fastapi.APIRouter()

router.include_router(habr.router, prefix="/habr")
router.include_router(jwt_auth.router, prefix="/habr")
