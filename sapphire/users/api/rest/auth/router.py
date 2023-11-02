import fastapi

from . import handlers, oauth2

router = fastapi.APIRouter()

router.add_api_route(methods=["GET"], path="/check", endpoint=handlers.check)
router.add_api_route(methods=["DELETE"], path="/logout", endpoint=handlers.logout)
router.include_router(oauth2.router, prefix="/oauth2")
