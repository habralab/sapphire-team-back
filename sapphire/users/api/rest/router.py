import fastapi

from . import auth, dependencies, users

router = fastapi.APIRouter(
    dependencies=[fastapi.Depends(dependencies.update_jwt)],
)

router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(users.router, prefix="/users", tags=["Users"])
