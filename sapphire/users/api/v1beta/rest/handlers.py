import uuid

import fastapi
from fastapi import Depends

from sapphire.common.api.jwt.depends import get_user_id
from sapphire.users.database.models import User
from sapphire.users.database.service import UsersDatabaseService

from .schemas import UserUpdateRequest, UserUpdateResponce

app = fastapi.FastAPI()


async def update(request: fastapi.Request,
                 user_id: uuid.UUID = Depends(get_user_id),
                 user: UserUpdateRequest = fastapi.Body(embed=False)) -> UserUpdateResponce:
    database_service: UsersDatabaseService = request.app.service.database

    if user.user_id != user_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDENT,
            detail="must be your user id",
        )

    async with database_service.transaction() as session:
        user_db = await database_service.update_user(
            user=User.id,
            session=session,
            first_name=user.first_name,
            last_name=user.last_name,
        )
    return UserUpdateResponce.model_validate(user_db)
