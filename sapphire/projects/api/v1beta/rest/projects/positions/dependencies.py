import uuid

import fastapi

from sapphire.projects.api.v1beta.rest.projects.dependencies import get_path_project
from sapphire.projects.database.models import Project
from sapphire.projects.database.service import ProjectsDatabaseService


async def get_path_position(
        request: fastapi.Request,
        project: Project = fastapi.Depends(get_path_project),
        position_id: uuid.UUID = fastapi.Path(),
):
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        position = await database_service.get_project_position(
            session=session,
            project_id=project.id,
            position_id=position_id,
        )
    if position is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Project position not found.",
        )

    return position
