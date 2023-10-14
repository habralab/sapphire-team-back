import uuid

import fastapi

from sapphire.common.jwt.dependencies.rest import auth_user_id
from sapphire.projects.database.service import ProjectsDatabaseService

from .schemas import (
    CreateProjectRequest,
    ProjectHistoryListResponse,
    ProjectHistoryResponse,
    ProjectInfoResponse,
    ProjectResponse,
)


async def create_project(
    request: fastapi.Request,
    request_user_id: uuid.UUID = fastapi.Depends(auth_user_id),
    data: CreateProjectRequest = fastapi.Body(embed=False),
) -> ProjectResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    if data.owner_id != request_user_id:
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


async def get(
    request: fastapi.Request,
    project_id: uuid.UUID,
) -> ProjectInfoResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        project_db = await database_service.get_project(
            session=session, project_id=project_id
        )
        last_history_db = await database_service.get_project_history(
            session=session, project_id=project_id, last=True
        )

    if project_db is None or last_history_db is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Cannot find project with this `project_id`",
        )

    return ProjectInfoResponse(
        project=ProjectResponse.model_validate(project_db),
        last_history=ProjectHistoryResponse.model_validate(last_history_db),
    )


async def history(
    request: fastapi.Request,
    project_id: uuid.UUID,
) -> ProjectHistoryListResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        history_db = await database_service.get_project_history(
            session=session, project_id=project_id
        )

    if history_db is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Cannot find project history with this `project_id`",
        )

    return ProjectHistoryListResponse(history=history_db)
