import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route("/", methods=["POST"], endpoint=handlers.create_review)
