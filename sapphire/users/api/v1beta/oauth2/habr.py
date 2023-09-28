import fastapi
import yarl
from fastapi.responses import RedirectResponse

router = fastapi.APIRouter()


@router.get("/authorize", response_class=RedirectResponse)
async def authorize(request: fastapi.Request):
    redirect_url = yarl.URL(str(request.url)).parent / "callback"

    # Get OAuth2 backend from request.app.habr_oauth2

@router.get("/callback")
async def callback():
    pass
