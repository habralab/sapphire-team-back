import fastapi

from sapphire.common.api.schemas import ErrorResponse, ResponseStatus
from sapphire.users.api.schemas import JWTTokensResponse

from sapphire.users.jwt import JWTMethods

router = fastapi.APIRouter()


@router.get("/", response_model=JWTTokensResponse | ErrorResponse)
async def issue_tokens(request: fastapi.Request, response: fastapi.Response):
    jwt_methods: JWTMethods = request.app.service.jwt_methods
    if request.query_params.get("user_id", None) is None:
        return ErrorResponse(message="Missing user id")
    access_token = jwt_methods.issue_access_token(request.query_params.get("user_id"))
    refresh_token = jwt_methods.issue_refresh_token(request.query_params.get("user_id"))
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
