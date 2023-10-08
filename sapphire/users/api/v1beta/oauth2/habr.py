import fastapi
import yarl
from fastapi.responses import RedirectResponse

from sapphire.common.api.jwt import JWTMethods
from sapphire.users.api.schemas import JWTTokensResponse

from sapphire.users.database.service import UsersDatabaseService
from sapphire.users.jwt import JWTMethods
from sapphire.users.oauth2.habr import HabrUser, OAuth2HabrBackend


router = fastapi.APIRouter()


@router.get("/authorize", response_class=RedirectResponse)
async def authorize(request: fastapi.Request):
    habr_oauth2: OAuth2HabrBackend = request.app.service.habr_oauth2

    redirect_url = yarl.URL(request.app.extra["root_url"])
    redirect_url /= request.url.path.lstrip("/")
    redirect_url = redirect_url.parent / "callback"
    authorization_url = habr_oauth2.get_authorization_url(
        redirect_url=str(redirect_url),
    )

    return authorization_url


@router.get("/callback", name="callback")
async def callback(
    state: str, code: str, request: fastapi.Request, response: fastapi.Response
) -> JWTTokensResponse:
    habr_oauth2: OAuth2HabrBackend = request.app.service.habr_oauth2
    jwt_methods: JWTMethods = request.app.service.jwt_methods
    database_service: UsersDatabaseService = request.app.service.database

    token = await habr_oauth2.get_token(state, code)
    if token is None:
        raise fastapi.HTTPException(status_code=401, detail="Not authenticated")

    habr_user: HabrUser = await habr_oauth2.get_user_info(token)
    await database_service.get_or_create_user(
        user_id=habr_user.id, user_email=habr_user.email
    )

    access_token = jwt_methods.issue_access_token(habr_user.id)
    refresh_token = jwt_methods.issue_refresh_token(habr_user.id)
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
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.delete("/logout")
def logout(response: fastapi.Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
