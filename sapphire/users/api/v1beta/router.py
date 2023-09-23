import fastapi

from .handlers.health import health


router = fastapi.APIRouter()

router.add_route(methods=["GET"], path="/health", endpoint=health)
