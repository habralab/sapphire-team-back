import uuid

import fastapi

from sapphire.common.jwt.dependencies.rest import auth_user_id
from sapphire.projects.database.models import Project
from sapphire.projects.database.service import ProjectsDatabaseService


async def get_path_project(
        request: fastapi.Request,
        project_id: uuid.UUID = fastapi.Path(),
) -> Project:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_project = await database_service.get_project(session=session, project_id=project_id)
    if db_project is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return db_project


async def path_project_is_owner(
        request_user_id: uuid.UUID = fastapi.Depends(auth_user_id),
        project: Project = fastapi.Depends(get_path_project),
) -> Project:
    if project.owner_id != request_user_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Forbidden."
        )

    return project
