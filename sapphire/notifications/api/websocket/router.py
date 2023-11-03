import fastapi

from . import notifications

router = fastapi.APIRouter()

router.add_api_websocket_route(path="/notifications", endpoint=notifications.notifications)
