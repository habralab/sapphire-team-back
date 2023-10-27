import fastapi

from . import logout, oauth2

router = fastapi.APIRouter()

router.add_api_route(methods=["DELETE"], path="/logout", endpoint=logout.logout)
router.include_router(oauth2.router, prefix="/oauth2")
