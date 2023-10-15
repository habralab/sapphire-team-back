import uuid

import fastapi

from sapphire.common.api.exceptions import HTTPNotAuthenticated
from sapphire.common.jwt.dependencies.rest import auth_user_id, get_request_user_id
from sapphire.users.database.models import User
from sapphire.users.database.service import UsersDatabaseService


async def get_path_user(
        request: fastapi.Request,
        user_id: uuid.UUID = fastapi.Path(),
) -> User:
    database: UsersDatabaseService = request.app.service.database

    async with database.transaction() as session:
        db_user = await database.get_user(session=session, user_id=user_id)
    if db_user is None:
        raise fastapi.exceptions.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return db_user


async def get_request_user(
        request: fastapi.Request,
        request_user_id: uuid.UUID | None = fastapi.Depends(get_request_user_id),
) -> User | None:
    if request_user_id is None:
        return None

    database: UsersDatabaseService = request.app.service.database
    async with database.transaction() as session:
        return await database.get_user(session=session, user_id=request_user_id)


async def auth_user(
        request: fastapi.Request,
        request_user_id: uuid.UUID = fastapi.Depends(auth_user_id),
):
    database: UsersDatabaseService = request.app.service.database

    async with database.transaction() as session:
        user = await database.get_user(session=session, user_id=request_user_id)
    if user is None:
        raise HTTPNotAuthenticated()

    return user
