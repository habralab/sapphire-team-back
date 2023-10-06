import fastapi

from . import health, projects

router = fastapi.APIRouter()

router.add_api_route(path="/health", endpoint=health.health)
router.include_router(projects.router, prefix="/projects")
