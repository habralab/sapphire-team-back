import uuid

import fastapi

from sapphire.common.jwt.dependencies.rest import auth, get_user_id
from sapphire.users.api.schemas.users import UserFullResponse, UserResponse, UserUpdateRequest
from sapphire.users.database.models import User
from sapphire.users.database.service import UsersDatabaseService

from .dependencies import get_user


async def get_user_handler(
        request_user_id: uuid.UUID = fastapi.Depends(get_user_id),
        user: User = fastapi.Depends(get_user),
) -> UserResponse | UserFullResponse:
    model_cls = UserResponse if request_user_id == user.id else UserFullResponse

    return model_cls.from_db_model(user)


async def update_user(
        request: fastapi.Request,
        request_user_id: uuid.UUID = fastapi.Depends(auth),
        user: User = fastapi.Depends(get_user),
        data: UserUpdateRequest = fastapi.Body(embed=False),
) -> UserFullResponse:
    if user.id != request_user_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Forbidden.",
        )

    database_service: UsersDatabaseService = request.app.service.database
    async with database_service.transaction() as session:
        user = await database_service.update_user(
            user=user,
            session=session,
            first_name=data.first_name,
            last_name=data.last_name,
            main_specialization_id=data.main_specialization_id,
            secondary_specialization_id=data.secondary_specialization_id
        )

    return UserFullResponse.from_db_model(user)
