import fastapi
import yarl
from fastapi.responses import RedirectResponse
from sapphire.users.oauth2.base import OAuth2BaseBackend
from sapphire.users.oauth2.habr import get_oauth2_backend, UsersSettings

router = fastapi.APIRouter()


@router.get("/authorize", response_class=RedirectResponse)
async def authorize(request: fastapi.Request, client_id: str, client_secret: str):
    redirect_url = yarl.URL(str(request.url)).parent / "callback"
    backend = OAuth2BaseBackend(client_id=client_id, client_secret=client_secret)
    authorisation_url = backend.get_authorization_url(redirect_url=str(redirect_url))
    return RedirectResponse(url=authorisation_url)
    # Get OAuth2 backend from request.app.habr_oauth2


@router.get("/callback")
async def callback(client_id: str, client_secret: str, state: str, code: str):
    settings = UsersSettings(habr_oauth2_client_id=client_id, habr_oauth2_client_secret=client_secret)
    backend = get_oauth2_backend(settings)
    token = await backend.get_token(state=state, code=code)
    user_info = await backend.get_user_info(token=token)
    return user_info