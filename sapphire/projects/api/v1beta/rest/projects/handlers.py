import uuid

import fastapi

from sapphire.common.jwt.dependencies.rest import get_user_id
from sapphire.projects.database.service import ProjectsDatabaseService

from .schemas import CreateProjectRequest, ProjectResponse


async def create(
    request: fastapi.Request,
    user_id: uuid.UUID = fastapi.Depends(get_user_id),
    project: CreateProjectRequest = fastapi.Body(embed=False),
) -> ProjectResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    if project.owner_id != user_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Field `owner_id` must be your user id",
        )

    async with database_service.transaction() as session:
        project_db = await database_service.create_project(
            session=session,
            name=project.name,
            owner_id=project.owner_id,
            description=project.description,
            deadline=project.deadline,
        )

    return ProjectResponse.model_validate(project_db)
