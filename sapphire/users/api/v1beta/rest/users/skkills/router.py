import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/skills", methods=["POST"],  endpoint=handlers.slills_installation)
