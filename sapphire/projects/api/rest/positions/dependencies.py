import uuid

import fastapi

from sapphire.common.api.exceptions import HTTPForbidden, HTTPNotFound
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.projects import database
from sapphire.projects.database.models import Position


async def get_path_position(
        request: fastapi.Request,
        position_id: uuid.UUID = fastapi.Path(),
) -> Position:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        position = await database_service.get_position(
            session=session,
            position_id=position_id,
        )
    if position is None:
        raise HTTPNotFound()

    return position


async def path_position_is_owner(
        jwt_data: JWTData = fastapi.Depends(is_auth),
        position: Position = fastapi.Depends(get_path_position),
) -> Position:
    if position.project.owner_id != jwt_data.user_id:
        raise HTTPForbidden()

    return position
