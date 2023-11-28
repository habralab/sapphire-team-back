import fastapi

from . import handlers

router = fastapi.APIRouter()

router.add_api_route(path="/", methods=["GET"], endpoint=handlers.get_notifications)
router.add_api_route(path="/count", methods=["GET"], endpoint=handlers.get_notifications_count)
router.add_api_route(path="/{notification_id}", methods=["GET"], endpoint=handlers.get_notification)
router.add_api_route(path="/{notification_id}", methods=["POST"],
                     endpoint=handlers.update_notification)
