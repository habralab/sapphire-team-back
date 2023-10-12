import fastapi

from . import health, oauth2, rest

router = fastapi.APIRouter()

router.add_api_route(methods=["GET"], path="/health", endpoint=health.health)
router.include_router(oauth2.router, prefix="/oauth2")
router.include_router(rest.router)
