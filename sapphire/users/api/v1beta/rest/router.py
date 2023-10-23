import fastapi

from . import auth, health, users

router = fastapi.APIRouter()

router.add_api_route(path="/health", endpoint=health.health)
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(users.router, prefix="/users", tags=["Users"])
