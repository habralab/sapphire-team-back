import fastapi

from sapphire.common.api.utils import set_cookie
from sapphire.common.jwt.dependencies.rest import get_jwt_data
from sapphire.common.jwt.methods import JWTMethods
from sapphire.common.jwt.models import JWTData
from sapphire.users.database.models import User
from sapphire.users.database.service import UsersDatabaseService


async def get_jwt_user(
        request: fastapi.Request,
        jwt_data: JWTData | None = fastapi.Depends(get_jwt_data),
):
    if jwt_data is None:
        return None

    database: UsersDatabaseService = request.app.service.database
    async with database.transaction() as session:
        return await database.get_user(session=session, user_id=jwt_data.user_id)


async def update_jwt(
        request: fastapi.Request,
        response: fastapi.Response,
        jwt_data: JWTData | None = fastapi.Depends(get_jwt_data),
        user: User = fastapi.Depends(get_jwt_user),
):
    yield

    if jwt_data is not None and jwt_data.is_activated != user.is_activated:
        jwt_methods: JWTMethods = request.app.service.jwt_methods

        access_token = jwt_methods.issue_access_token(user_id=user.id,
                                                      is_activated=user.is_activated)
        refresh_token = jwt_methods.issue_refresh_token(user_id=user.id,
                                                        is_activated=user.is_activated)

        response = set_cookie(response=response, name="access_token", value=access_token,
                              expires=jwt_methods.access_token_expires_utc)
        response = set_cookie(response=response, name="refresh_token", value=refresh_token,
                              expires=jwt_methods.refresh_token_expires_utc)
