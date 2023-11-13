import math
import pathlib

import aiofiles
import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.api.exceptions import HTTPForbidden
from sapphire.common.jwt.dependencies.rest import is_activated
from sapphire.common.jwt.models import JWTData
from sapphire.projects.database.models import Project
from sapphire.projects.database.service import ProjectsDatabaseService

from .dependencies import get_path_project, path_project_is_owner
from .schemas import (
    CreateProjectRequest,
    ProjectHistoryListResponse,
    ProjectHistoryResponse,
    ProjectListFiltersRequest,
    ProjectListResponse,
    ProjectPartialUpdateRequest,
    ProjectResponse,
    CreateProjectResponse,
)

from loguru import logger
async def create_project(
    request: fastapi.Request,
    jwt_data: JWTData = fastapi.Depends(is_activated),
    data: CreateProjectRequest = fastapi.Body(embed=False),
) -> CreateProjectResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    if data.owner_id != jwt_data.user_id:
        raise HTTPForbidden()

    async with database_service.transaction() as session:
        project_db = await database_service.create_project(
            session=session,
            name=data.name,
            owner_id=data.owner_id,
            description=data.description,
            deadline=data.deadline,
        )
    logger.info("AAAAAAAAAAAAAAAAA")
    logger.info(project_db.__dict__)
    return CreateProjectResponse.model_validate(project_db)


async def get_projects(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    filters: ProjectListFiltersRequest = fastapi.Depends(ProjectListFiltersRequest),
) -> ProjectListResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        projects_db = await database_service.get_projects(
            session=session,
            page=pagination.page,
            per_page=pagination.per_page,
            **filters.model_dump(),
        )

    projects = [ProjectResponse.model_validate(project_db) for project_db in projects_db]

    return ProjectListResponse(data=projects, page=pagination.page, per_page=pagination.per_page)


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


async def partial_update_project(
    request: fastapi.Request,
    project: Project = fastapi.Depends(path_project_is_owner),
    data: ProjectPartialUpdateRequest = fastapi.Body(embed=False)
) -> ProjectResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        project = await database_service.update_project(
            session=session,
            project=project,
            status=data.status,
        )

    return ProjectResponse.model_validate(project)


async def upload_project_avatar(
        request: fastapi.Request,
        project: Project = fastapi.Depends(path_project_is_owner),
        avatar: fastapi.UploadFile = fastapi.File(...),
) -> ProjectResponse:

    database_service: ProjectsDatabaseService = request.app.service.database
    media_dir_path: pathlib.Path = request.app.service.media_dir_path
    load_file_chunk_size: int = request.app.service.load_file_chunk_size

    avatars_dir_path: pathlib.Path = media_dir_path / "project-avatars"
    avatar_file_path = avatars_dir_path / f"project-{project.id}"

    await aiofiles.os.makedirs(avatars_dir_path, exist_ok=True)
    async with aiofiles.open(avatar_file_path, "wb") as avatar_file:
        while content := await avatar.read(size=load_file_chunk_size):
            await avatar_file.write(content)

    async with database_service.transaction() as session:
        project = await database_service.update_project(
            session=session,
            project=project,
            avatar=str(avatar_file_path),
        )

    return ProjectResponse.model_validate(project)


async def delete_project_avatar(
        request: fastapi.Request,
        project: Project = fastapi.Depends(path_project_is_owner),
) -> ProjectResponse:

    if project.avatar is not None:
        database_service: ProjectsDatabaseService = request.app.service.database
        original_avatar_file_path = project.avatar
        async with database_service.transaction() as session:
            project = await database_service.update_project(
                session=session,
                project=project,
                avatar=None,
            )

        await aiofiles.os.remove(original_avatar_file_path)

    return ProjectResponse.model_validate(project)
