import math
import uuid
from datetime import datetime

import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.jwt.dependencies.rest import auth_user_id
from sapphire.projects.database.models import Project, ProjectStatusEnum
from sapphire.projects.database.service import ProjectsDatabaseService

from .dependencies import get_path_project
from .schemas import (
    CreateProjectRequest,
    ProjectHistoryListResponse,
    ProjectHistoryResponse,
    ProjectResponse,
    ProjectsResponse,
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


async def get_project(
    project: Project = fastapi.Depends(get_path_project),
) -> ProjectResponse:
    return ProjectResponse.model_validate(project)


async def history(
    project: Project = fastapi.Depends(get_path_project),
    pagination: Pagination = fastapi.Depends(pagination),
) -> ProjectHistoryListResponse:
    offset = (pagination.page - 1) * pagination.per_page
    history = [
        ProjectHistoryResponse.model_validate(event)
        for event in project.history[offset : offset + pagination.per_page]
    ]
    total_items = len(project.history)
    total_pages = int(math.ceil(total_items / pagination.per_page))
    return ProjectHistoryListResponse(
        data=history,
        page=pagination.page,
        per_page=pagination.per_page,
        total_pages=total_pages,
        total_items=total_items,
    )


async def get_projects(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    project_name_substring: str | None = None,
    project_description_substring: str | None = None,
    project_owner_id: uuid.UUID | None = None,
    project_deadline: datetime | None = None,
    project_status: ProjectStatusEnum | None = None,
    position_name_substring: str | None = None,
    position_is_deleted: bool | None = None,
    position_is_closed: bool | None = None,
) -> ProjectsResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    filters = {}
    if project_name_substring:
        filters["project_name_substring"] = project_name_substring
    if project_description_substring:
        filters["project_description_substring"] = project_description_substring
    if project_owner_id:
        filters["project_owner_id"] = project_owner_id
    if project_deadline:
        filters["project_deadline"] = project_deadline
    if project_status:
        filters["project_status"] = project_status
    if position_name_substring:
        filters["position_name_substring"] = position_name_substring
    if position_is_deleted:
        filters["position_is_deleted"] = position_is_deleted
    if position_is_closed:
        filters["position_is_closed"] = position_is_closed

    async with database_service.transaction() as session:
        projects_db = await database_service.get_projects(
            session=session,
            page=pagination.page,
            per_page=pagination.per_page,
            **filters,
        )

    projects = [ProjectResponse.model_validate(project_db) for project_db in projects_db]

    return ProjectsResponse(data=projects, page=pagination.page, per_page=pagination.per_page)
