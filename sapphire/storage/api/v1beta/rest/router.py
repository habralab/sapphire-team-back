import fastapi

from . import health, specializations

router = fastapi.APIRouter()

router.add_api_route(path="/health", endpoint=health.health)
router.add_api_route(path="/specializations", endpoint=specializations.get_specializations)
router.add_api_route(path="/spec-groups", endpoint=specializations.get_specialization_groups)
