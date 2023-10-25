import math
import pathlib
import uuid

import aiofiles
import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.jwt.dependencies.rest import auth_user_id
from sapphire.projects.database.models import Project
from sapphire.projects.database.service import ProjectsDatabaseService

from .dependencies import get_path_project, path_project_is_owner
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
) -> ProjectsResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        projects_db = await database_service.get_projects(
            session=session,
            page=pagination.page,
            per_page=pagination.per_page,
        )

    projects = [ProjectResponse.model_validate(project_db) for project_db in projects_db]

    return ProjectsResponse(data=projects, page=pagination.page, per_page=pagination.per_page)


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
