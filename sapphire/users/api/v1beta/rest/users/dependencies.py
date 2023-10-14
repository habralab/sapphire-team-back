import uuid

import fastapi

from sapphire.users.database.models import User
from sapphire.users.database.service import UsersDatabaseService


async def get_user(
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
