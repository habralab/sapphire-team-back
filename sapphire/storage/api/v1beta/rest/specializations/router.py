import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/", endpoint=handlers.get_specializations)
