import fastapi
import yarl
from fastapi.responses import RedirectResponse

from sapphire.common.api.schemas import ErrorResponse, ResponseStatus
from sapphire.users.api.schemas import JWTTokensResponse
from sapphire.users.jwt import JWTMethods
from sapphire.users.oauth2.habr import OAuth2HabrBackend

router = fastapi.APIRouter()


@router.get("/authorize", response_class=RedirectResponse)
async def authorize(request: fastapi.Request):
    habr_oauth2: OAuth2HabrBackend = request.app.service.habr_oauth2
    redirect_url = yarl.URL(str(request.url)).parent / "callback"
    authorization_url = habr_oauth2.get_authorization_url(redirect_url=str(redirect_url))
    return authorization_url


@router.get("/callback", response_model=JWTTokensResponse | ErrorResponse)
async def callback(request: fastapi.Request, response: fastapi.Response):
    habr_oauth2: OAuth2HabrBackend = request.app.service.habr_oauth2
    jwt_methods: JWTMethods = request.app.service.jwt_methods
    token = await habr_oauth2.get_token()
    if token is None:
        return ErrorResponse(message="Client cannot receive oauth2 access token")
    user_info = await habr_oauth2.get_user_info(token=token)
    access_token = jwt_methods.issue_access_token(user_info.id)
    refresh_token = jwt_methods.issue_refresh_token(user_info.id)
    add_to_cookies = [
        ("access_token", access_token, jwt_methods.access_token_expires),
        ("refresh_token", refresh_token, jwt_methods.refresh_token_expires),
    ]
    for name, token, expires in add_to_cookies:
        response.set_cookie(
            key=name,
            value=token,
            expires=expires,
            path="/",
            secure=True,
            httponly=True,
            samesite="none",
        )

    return JWTTokensResponse(
        status=ResponseStatus.OK,
        access_token=access_token,
        refresh_token=refresh_token,
    )
