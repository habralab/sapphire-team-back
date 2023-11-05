import fastapi

from . import projects, users

router = fastapi.APIRouter()

router.include_router(projects.router, prefix="/projects", tags=["Projects"])
router.include_router(users.router, prefix="/users", tags=["Users"])
