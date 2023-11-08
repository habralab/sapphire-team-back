import fastapi
from fastapi.responses import RedirectResponse

from sapphire.common.habr import HabrClient
from sapphire.common.habr_career import HabrCareerClient
from sapphire.common.jwt import JWTMethods
from sapphire.users.api.rest.auth.schemas import AuthorizeResponse
from sapphire.users.database.service import UsersDatabaseService
from sapphire.users.oauth2.habr import OAuth2HabrBackend

router = fastapi.APIRouter()


@router.get("/authorize", response_class=RedirectResponse)
async def authorize(
        request: fastapi.Request,
        redirect_url: str | None = fastapi.Query(None),
):
    habr_oauth2: OAuth2HabrBackend = request.app.service.habr_oauth2
    habr_oauth2_callback_url: str = request.app.service.habr_oauth2_callback_url

    if redirect_url is None:
        redirect_url = habr_oauth2_callback_url
    authorization_url = habr_oauth2.get_authorization_url(
        redirect_url=redirect_url,
    )

    return authorization_url


@router.get("/callback", name="callback")
async def callback(
    state: str, code: str, request: fastapi.Request, response: fastapi.Response
) -> AuthorizeResponse:
    habr_client: HabrClient = request.app.service.habr_client
    habr_career_client: HabrCareerClient = request.app.service.habr_career_client
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
        habr_user_info = await habr_client.get_user_card(username=habr_user.login)
        habr_career_user_info = await habr_career_client.get_career_track(user_id=habr_user.id)

        habr_user_full_name = habr_career_user_info.full_name or habr_user_info.full_name
        first_name, last_name = None, None
        if habr_user_full_name is not None:
            first_name, *last_name = habr_user_full_name.split(maxsplit=1)
            last_name = last_name[0] if last_name else None

        async with database_service.transaction() as session:
            db_user = await database_service.create_user(
                session=session,
                email=habr_user.email,
                first_name=first_name,
                last_name=last_name,
            )

    access_token = jwt_methods.issue_access_token(db_user.id)
    refresh_token = jwt_methods.issue_refresh_token(db_user.id)

    cookies = [
        ("access_token", access_token, jwt_methods.access_token_expires_for_cookie),
        ("refresh_token", refresh_token, jwt_methods.refresh_token_expires_for_cookie),
    ]
    for name, token, expires in cookies:
        response.set_cookie(
            key=name,
            value=token,
            expires=expires,
            path="/",
            secure=True,
            httponly=True,
            samesite="strict",
        )

    return AuthorizeResponse(
        user_id=db_user.id,
        access_token=access_token,
        refresh_token=refresh_token,
    )
