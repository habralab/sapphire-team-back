import fastapi

from collabry.common.api.utils import set_cookie
from collabry.common.jwt.dependencies.rest import get_jwt_data
from collabry.common.jwt.methods import JWTMethods
from collabry.common.jwt.models import JWTData
from collabry.database.models import User
from collabry.users import database


async def get_jwt_user(
        request: fastapi.Request,
        jwt_data: JWTData | None = fastapi.Depends(get_jwt_data),
):
    if jwt_data is None:
        return None

    database_service: database.Service = request.app.service.database
    async with database_service.transaction() as session:
        return await database_service.get_user(session=session, user_id=jwt_data.user_id)


async def update_jwt(
        request: fastapi.Request,
        response: fastapi.Response,
        jwt_data: JWTData | None = fastapi.Depends(get_jwt_data),
        user: User | None = fastapi.Depends(get_jwt_user),
):
    if jwt_data is None or user is None or jwt_data.is_activated == user.is_activated:
        return

    jwt_methods: JWTMethods = request.app.service.jwt_methods

    access_token = jwt_methods.issue_access_token(user_id=user.id, is_activated=user.is_activated)
    refresh_token = jwt_methods.issue_refresh_token(user_id=user.id, is_activated=user.is_activated)

    response = set_cookie(response=response, name="access_token", value=access_token,
                          expires=jwt_methods.access_token_expires_utc)
    response = set_cookie(response=response, name="refresh_token", value=refresh_token,
                          expires=jwt_methods.refresh_token_expires_utc)
