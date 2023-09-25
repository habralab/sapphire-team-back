import fastapi

from . import v1beta


router = fastapi.APIRouter()

router.include_router(v1beta.router, prefix="/v1beta")
