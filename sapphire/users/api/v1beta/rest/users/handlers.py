import uuid

import fastapi

from sapphire.common.jwt.dependencies.rest import auth, get_user_id
from sapphire.users.api.schemas.users import UserFullResponse, UserResponse, UserUpdateRequest
from sapphire.users.database.service import UsersDatabaseService


async def get_user(
        request: fastapi.Request,
        request_user_id: uuid.UUID = fastapi.Depends(get_user_id),
        user_id: uuid.UUID = fastapi.Path(),
) -> UserResponse | UserFullResponse:
    database_service: UsersDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        user_db = await database_service.get_user(session=session, user_id=user_id)
        if user_db is None:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

    model_cls = UserResponse if request_user_id is None else UserFullResponse
    return model_cls.model_validate(user_db)


async def update_user(
        request: fastapi.Request,
        request_user_id: uuid.UUID = fastapi.Depends(auth),
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
    return UserFullResponse(
        id=user_db.id,
        email=user_db.email,
        first_name=user_db.first_name,
        last_name=user_db.last_name,
        about=user_db.profile.about,
        main_specialization_id=user_db.profile.main_specialization_id,
        secondary_specialization_id=user_db.profile.secondary_specialization_id,
        created_at=user_db.created_at,
        updated_at=user_db.updated_at,
    )
