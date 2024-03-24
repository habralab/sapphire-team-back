import fastapi

from . import change_password, handlers, oauth2

router = fastapi.APIRouter()

router.add_api_route(methods=["GET"], path="/check", endpoint=handlers.check)
router.add_api_route(methods=["DELETE"], path="/logout", endpoint=handlers.logout)
router.add_api_route(methods=["POST"], path="/signup", endpoint=handlers.sign_up)
router.add_api_route(methods=["POST"], path="/signin", endpoint=handlers.sign_in)
router.include_router(oauth2.router, prefix="/oauth2")
router.include_router(change_password.router, prefix="/change_password")
