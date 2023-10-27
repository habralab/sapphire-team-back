import fastapi

from . import skills, specialization_groups, specializations

router = fastapi.APIRouter()

router.include_router(skills.router, prefix="/skills", tags=["Skills"])
router.include_router(specializations.router, prefix="/specializations", tags=["Specializations"])
router.include_router(specialization_groups.router, prefix="/spec-groups",
                      tags=["Specialization Groups"])
