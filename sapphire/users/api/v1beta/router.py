import fastapi

from . import health, oauth2

router = fastapi.APIRouter()

router.add_route(methods=["GET"], path="/health", endpoint=health.health)
router.include_router(oauth2.router, prefix="/oauth2")
