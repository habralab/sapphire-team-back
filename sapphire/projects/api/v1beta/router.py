import fastapi

from . import health


router = fastapi.APIRouter()

router.add_api_route(path="/health", endpoint=health.health)
