import fastapi
from sapphire.notifications.api.rest import handlers


router = fastapi.APIRouter()


router.add_route(path="/notifications", methods=["GET"], endpoint=handlers.get_notifications)
