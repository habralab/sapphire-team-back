import uuid

import fastapi

from sapphire.common.jwt.dependencies.rest import get_request_user_id


async def logout(response: fastapi.Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")


async def check(
        request_user_id: uuid.UUID | None = fastapi.Depends(get_request_user_id),
) -> bool:
    return request_user_id is not None
