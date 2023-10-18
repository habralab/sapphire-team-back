import uuid

import fastapi

from sapphire.users.api.v1beta.rest.users.dependencies import auth_user_id, get_path_user
from sapphire.users.api.v1beta.rest.users.handlers import get_user
from sapphire.users.database.models import User
from sapphire.users.database.service import UsersDatabaseService


async def slills_installation(
        request: fastapi.Request,
        new_userskills_ids: list[uuid.UUID] = fastapi.Body(embed=False),  ##??????
        path_user_id: uuid.UUID | None = fastapi.Depends(get_path_user),
        request_user_id: uuid.UUID | None = fastapi.Depends(auth_user_id),
        user: User = fastapi.Depends(get_user), ):
    if path_user_id != request_user_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Forbidden.",
        )
    database_service: UsersDatabaseService = request.app.service.database
    async with database_service.transaction() as session:
        skill = await database_service.update_user_skills(
            session=session,
            user=user,
            new_userskills_ids=new_userskills_ids
        )
    return skill
