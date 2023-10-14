import uuid

import fastapi

from sapphire.common.jwt.dependencies.rest import auth
from sapphire.projects.database.service import ProjectsDatabaseService

from .schemas import CreateProjectRequest, ProjectResponse


async def create_project(
    request: fastapi.Request,
    user_id: uuid.UUID = fastapi.Depends(auth),
    data: CreateProjectRequest = fastapi.Body(embed=False),
) -> ProjectResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    if data.owner_id != user_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Field `owner_id` must be your user id",
        )

    async with database_service.transaction() as session:
        project_db = await database_service.create_project(
            session=session,
            name=data.name,
            owner_id=data.owner_id,
            description=data.description,
            deadline=data.deadline,
        )

    return ProjectResponse.model_validate(project_db)
