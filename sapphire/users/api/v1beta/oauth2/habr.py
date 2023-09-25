import fastapi
import yarl
from fastapi.responses import RedirectResponse


router = fastapi.APIRouter()


@router.get("/authorize", response_class=RedirectResponse)
async def authorize(request: fastapi.Request):
    service = request.app.service
    callback_url = yarl.URL(str(request.url)).parent / "callback"

    service


@router.get("/callback")
async def callback():
    pass
