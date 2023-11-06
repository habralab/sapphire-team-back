import uuid

import fastapi

from sapphire.projects.database import ProjectsDatabaseService
from sapphire.projects.database.models import Position
from sapphire.projects.api.rest.projects.positions.dependencies import get_path_position


async def update_project_position_skills(
        request: fastapi.Request,
        position: Position = fastapi.Depends(get_path_position),
        data: set[uuid.UUID] = fastapi.Body(embed=False),
) -> set[uuid.UUID]:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        skills = await database_service.update_project_position_skills(
            session=session,
            position=position,
            skills=data,
        )

    return skills
