import uuid

import fastapi

from sapphire.common.jwt.dependencies.rest import get_user_id
from sapphire.users.api.schemas.users import UserFullResponse, UserUpdateRequest
from sapphire.users.database.service import UsersDatabaseService


async def update_user(
        request: fastapi.Request,
        request_user_id: uuid.UUID = fastapi.Depends(get_user_id),
        user_id: uuid.UUID = fastapi.Path(),
        user: UserUpdateRequest = fastapi.Body(embed=False),
) -> UserFullResponse:
    database_service: UsersDatabaseService = request.app.service.database

    if user_id != request_user_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Forbidden.",
        )

    async with database_service.transaction() as session:
        user_db = await database_service.get_user(session=session, user_id=user_id)
        if user_db is None:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        user_db = await database_service.update_user(
            user=user_db,
            session=session,
            first_name=user.first_name,
            last_name=user.last_name,
        )
    return UserFullResponse.model_validate(user_db)
