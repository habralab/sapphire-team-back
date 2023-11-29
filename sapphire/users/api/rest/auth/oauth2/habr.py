import asyncio

import fastapi
from fastapi.responses import RedirectResponse

from sapphire.common.api.utils import set_cookie
from sapphire.common.habr import HabrClient
from sapphire.common.habr_career import HabrCareerClient
from sapphire.common.jwt import JWTMethods
from sapphire.users.api.rest.auth.schemas import AuthorizeResponse
from sapphire.users.api.rest.schemas import UserResponse
from sapphire.users.cache.service import UsersCacheService
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

    cache_service: UsersCacheService = request.app.service.cache

    state = await cache_service.set_state()

    if redirect_url is None:
        redirect_url = habr_oauth2_callback_url
    authorization_url = habr_oauth2.get_authorization_url(
        redirect_url=redirect_url,
        state=state,
    )

    return authorization_url


@router.get("/callback", name="callback")
async def callback(
        state: str,
        code: str,
        request: fastapi.Request,
        response: fastapi.Response,
) -> AuthorizeResponse:
    habr_client: HabrClient = request.app.service.habr_client
    habr_career_client: HabrCareerClient = request.app.service.habr_career_client
    habr_oauth2: OAuth2HabrBackend = request.app.service.habr_oauth2
    jwt_methods: JWTMethods = request.app.service.jwt_methods

    database_service: UsersDatabaseService = request.app.service.database

    token = await habr_oauth2.get_token(code=code)
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
        coros = [
            habr_client.get_user_card(username=habr_user.login),
            habr_career_client.get_career_track(user_id=habr_user.id),
        ]
        habr_user_info, habr_career_user_info = await asyncio.gather(*coros)
        first_name, last_name = None, None
        habr_user_full_name = (
            getattr(habr_career_user_info, "full_name", None) or
            getattr(habr_user_info, "full_name", None)
        )
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
            db_user.activate()

    access_token = jwt_methods.issue_access_token(db_user.id, is_activated=db_user.is_activated)
    refresh_token = jwt_methods.issue_refresh_token(db_user.id, is_activated=db_user.is_activated)

    response = set_cookie(response=response, name="access_token", value=access_token,
                          expires=jwt_methods.access_token_expires_utc)
    response = set_cookie(response=response, name="refresh_token", value=refresh_token,
                          expires=jwt_methods.refresh_token_expires_utc)

    return AuthorizeResponse(
        user=UserResponse.from_db_model(user=db_user),
        access_token=access_token,
        refresh_token=refresh_token,
    )
