import uuid

import fastapi

from sapphire.common.api.exceptions import HTTPForbidden, HTTPNotAuthenticated, HTTPNotFound
from sapphire.users.api.rest.dependencies import get_jwt_user
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
        raise HTTPNotFound()

    return db_user


async def is_auth_user(user: User | None = fastapi.Depends(get_jwt_user)):
    if user is None:
        raise HTTPNotAuthenticated()

    return user


async def is_activated_user(user: User = fastapi.Depends(is_auth_user)):
    if not user.is_activated:
        raise HTTPForbidden()

    return user
