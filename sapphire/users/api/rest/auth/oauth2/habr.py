import fastapi
from fastapi.responses import RedirectResponse

from sapphire.common.jwt import JWTMethods
from sapphire.users.api.rest.auth.schemas import JWTTokensResponse
from sapphire.users.database.service import UsersDatabaseService
from sapphire.users.oauth2.habr import OAuth2HabrBackend

router = fastapi.APIRouter()


@router.get("/authorize", response_class=RedirectResponse)
async def authorize(request: fastapi.Request):
    habr_oauth2: OAuth2HabrBackend = request.app.service.habr_oauth2
    habr_oauth2_callback_url: str = request.app.service.habr_oauth2_callback_url

    redirect_url = habr_oauth2_callback_url
    authorization_url = habr_oauth2.get_authorization_url(
        redirect_url=redirect_url,
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
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )

    habr_user = await habr_oauth2.get_user_info(token)
    async with database_service.transaction() as session:
        db_user = await database_service.get_user(
            session=session,
            email=habr_user.email,
        )
    if db_user is None:
        async with database_service.transaction() as session:
            db_user = await database_service.create_user(session=session, email=habr_user.email)

    access_token = jwt_methods.issue_access_token(db_user.id)
    refresh_token = jwt_methods.issue_refresh_token(db_user.id)

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
