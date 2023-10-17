import uuid

import fastapi

from sapphire.projects.api.v1beta.rest.projects.dependencies import get_path_project
from sapphire.projects.database.models import Position, Project
from sapphire.projects.database.service import ProjectsDatabaseService


async def get_path_position(
    request: fastapi.Request,
    position_id: uuid.UUID = fastapi.Path(),
) -> Position:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_position = await database_service.get_project_position(
            session=session, position_id=position_id
        )
    if db_position is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Position not found.",
        )

    return db_position


async def check_path_position(
    position: Position = fastapi.Depends(get_path_position),
    project: Project = fastapi.Depends(get_path_project),
) -> Position:
    if position.project_id != project.id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Position not found."
        )

    return position
