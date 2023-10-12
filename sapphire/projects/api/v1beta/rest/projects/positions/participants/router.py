import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(
    path="/request", methods=["POST"], endpoint=handlers.create_request_participate
)
router.add_api_route(
    path="/request", methods=["DELETE"], endpoint=handlers.remove_request_participate
)
