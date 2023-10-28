import fastapi

from . import projects

router = fastapi.APIRouter()

router.include_router(projects.router, prefix="/projects", tags=["Projects"])
