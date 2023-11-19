import fastapi

from . import positions, projects, reviews, users

router = fastapi.APIRouter()

router.include_router(positions.router, prefix="/positions", tags=["Positions"])
router.include_router(projects.router, prefix="/projects", tags=["Projects"])
router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
router.include_router(users.router, prefix="/users", tags=["Users"])
