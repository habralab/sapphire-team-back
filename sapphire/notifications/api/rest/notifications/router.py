import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["GET"], endpoint=handlers.get_notifications)
router.add_api_route(path="/{notification_id}", methods=["GET"], endpoint=handlers.get_notification)
