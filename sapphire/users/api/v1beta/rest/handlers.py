import uuid

import fastapi

from sapphire.users.database.service import UsersDatabaseService

from .schemas import UserUpdateRequest, UserUpdateResponce

app = fastapi.FastAPI()


async def update(request: fastapi.Request,
                 user_id: uuid.UUID,
                 user: UserUpdateRequest) -> UserUpdateResponce:
    database_service: UsersDatabaseService = request.app.service.database

    if user.user_id != user_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="must be your user id",
        )

    async with database_service.transaction() as session:
        user.db = await database_service.update_user(
            session=session,
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
        )
    return UserUpdateResponce.model_validate(user.db)
