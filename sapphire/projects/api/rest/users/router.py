import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/{user_id}/statistic", endpoint=handlers.get_user_statistic)
