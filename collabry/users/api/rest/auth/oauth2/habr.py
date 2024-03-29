import asyncio

import fastapi
from fastapi.responses import RedirectResponse

from collabry.common.habr import HabrClient
from collabry.common.habr_career import HabrCareerClient
from collabry.common.jwt import JWTMethods
from collabry.users import broker, cache, database, oauth2
from collabry.users.api.rest.auth.schemas import AuthorizeResponse
from collabry.users.api.rest.auth.utils import generate_authorize_response

router = fastapi.APIRouter()


@router.get("/authorize", response_class=RedirectResponse)
async def authorize(
        request: fastapi.Request,
        redirect_url: str | None = fastapi.Query(None),
):
    oauth2_habr: oauth2.habr.Service = request.app.service.oauth2_habr
    oauth2_habr_callback_url: str = request.app.service.oauth2_habr_callback_url

    cache_service: cache.Service = request.app.service.cache

    state = await cache_service.oauth_set_state()

    if redirect_url is None:
        redirect_url = oauth2_habr_callback_url
    authorization_url = oauth2_habr.get_authorization_url(
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
    oauth2_habr: oauth2.habr.Service = request.app.service.oauth2_habr
    jwt_methods: JWTMethods = request.app.service.jwt_methods

    broker_service: broker.Service = request.app.service.broker
    database_service: database.Service = request.app.service.database

    token = await oauth2_habr.get_token(code=code)
    if token is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )

    habr_user = await oauth2_habr.get_user_info(token)
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
            await broker_service.send_registration_email(user=db_user)

    return generate_authorize_response(jwt_methods=jwt_methods, response=response, user=db_user)
