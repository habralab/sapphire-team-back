import fastapi

from sapphire.common.jwt.dependencies.rest import get_jwt_data
from sapphire.common.jwt.models import JWTData


async def logout(response: fastapi.Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


async def check(jwt_data: JWTData | None = fastapi.Depends(get_jwt_data)) -> JWTData | None:
    return jwt_data
