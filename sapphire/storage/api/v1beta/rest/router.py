import fastapi

from . import health, skills, specialization_groups, specializations

router = fastapi.APIRouter()

router.add_api_route(path="/health", endpoint=health.health)
router.include_router(skills.router, prefix="/skills", tags=["Skills"])
router.include_router(specializations.router, prefix="/specializations", tags=["Specializations"])
router.include_router(specialization_groups.router, prefix="/spec-groups",
                      tags=["Specialization Groups"])
