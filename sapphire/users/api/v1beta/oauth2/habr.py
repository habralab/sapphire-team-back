import uuid

import fastapi
import yarl
from fastapi.responses import RedirectResponse

from sapphire.common.api.schemas import OKResponse
from sapphire.common.api.schemas.enums import ResponseStatus
from sapphire.users.api.schemas import JWTTokensResponse
from sapphire.users.jwt import JWTMethods
from sapphire.users.oauth2.habr import OAuth2HabrBackend

router = fastapi.APIRouter()


@router.get("/authorize", response_class=RedirectResponse)
async def authorize(request: fastapi.Request):
    habr_oauth2: OAuth2HabrBackend = request.app.service.habr_oauth2

    redirect_url = yarl.URL(request.app.extra["root_url"]) / request.app.root_path / "callback"
    authorization_url = habr_oauth2.get_authorization_url(
        redirect_url=str(redirect_url),
    )

    return authorization_url


@router.get("/callback")
async def callback(
    state: str, code: str, request: fastapi.Request, response: fastapi.Response
) -> JWTTokensResponse:
    habr_oauth2: OAuth2HabrBackend = request.app.service.habr_oauth2
    jwt_methods: JWTMethods = request.app.service.jwt_methods

    token = await habr_oauth2.get_token(state, code)
    if token is None:
        raise fastapi.HTTPException(status_code=401, detail="Not authenticated")

    user_id = uuid.uuid4()  # temporary solution, refactor will be later

    access_token = jwt_methods.issue_access_token(user_id)
    refresh_token = jwt_methods.issue_refresh_token(user_id)
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


@router.delete("/logout")
def logout(response: fastapi.Response) -> OKResponse:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return OKResponse()
