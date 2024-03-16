import fastapi

from sapphire.common.api.utils import set_cookie
from sapphire.common.jwt.methods import JWTMethods
from sapphire.database.models import User
from sapphire.users.api.rest.schemas import UserResponse

from .schemas import AuthorizeResponse


def generate_authorize_response(
        jwt_methods: JWTMethods,
        response: fastapi.Response,
        user: User,
) -> AuthorizeResponse:
    access_token = jwt_methods.issue_access_token(user.id, is_activated=user.is_activated)
    refresh_token = jwt_methods.issue_refresh_token(user.id, is_activated=user.is_activated)

    response = set_cookie(response=response, name="access_token", value=access_token,
                          expires=jwt_methods.access_token_expires_utc)
    response = set_cookie(response=response, name="refresh_token", value=refresh_token,
                          expires=jwt_methods.refresh_token_expires_utc)

    return AuthorizeResponse(
        user=UserResponse.from_db_model(user=user),
        access_token=access_token,
        refresh_token=refresh_token,
    )
