import fastapi
import yarl
from fastapi.responses import RedirectResponse

router = fastapi.APIRouter()


@router.get("/authorize", response_class=RedirectResponse)
async def authorize(request: fastapi.Request):
    habr_oauth2 = request.app.habr_oauth2
    redirect_url = yarl.URL(str(request.url)).parent / "callback"
    authorization_url = habr_oauth2.get_authorization_url(redirect_url=str(redirect_url))
    return authorization_url


@router.get("/callback")
async def callback(request: fastapi.Request):
    habr_oauth2 = request.app.habr_oauth2
    token = await habr_oauth2.get_token()
    user_info = await habr_oauth2.get_user_info(token=token)
    return user_info
