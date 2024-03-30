import uuid

import fastapi

from collabry.database.models import Position
from collabry.projects import database
from collabry.projects.api.rest.positions.dependencies import (
    get_path_position,
    path_position_is_owner,
)


async def update_position_skills(
        request: fastapi.Request,
        position: Position = fastapi.Depends(path_position_is_owner),
        data: set[uuid.UUID] = fastapi.Body(embed=False),
) -> set[uuid.UUID]:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        skills = await database_service.update_position_skills(
            session=session,
            position=position,
            skills=data,
        )

    return skills


async def get_position_skills(
        position: Position = fastapi.Depends(get_path_position),
) -> list[uuid.UUID]:
    return [skill.skill_id for skill in position.skills]
