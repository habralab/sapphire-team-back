import pathlib

import aiofiles
import fastapi
from fastapi.responses import FileResponse

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.api.exceptions import HTTPForbidden
from sapphire.common.jwt.dependencies.rest import is_activated
from sapphire.common.jwt.models import JWTData
from sapphire.projects import database
from sapphire.projects.api.rest.schemas import ProjectResponse
from sapphire.projects.database.models import Project

from .dependencies import get_path_project, path_project_is_owner
from .schemas import (
    CreateProjectRequest,
    ProjectHistoryListResponse,
    ProjectHistoryResponse,
    ProjectListFiltersRequest,
    ProjectListResponse,
    ProjectPartialUpdateRequest,
)


async def create_project(
    request: fastapi.Request,
    jwt_data: JWTData = fastapi.Depends(is_activated),
    data: CreateProjectRequest = fastapi.Body(embed=False),
) -> ProjectResponse:
    database_service: database.Service = request.app.service.database

    if data.owner_id != jwt_data.user_id:
        raise HTTPForbidden()

    async with database_service.transaction() as session:
        project_db = await database_service.create_project(
            session=session,
            name=data.name,
            owner_id=data.owner_id,
            description=data.description,
            startline=data.startline,
            deadline=data.deadline,
        )

    return ProjectResponse.model_validate(project_db)


async def get_projects(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    filters: ProjectListFiltersRequest = fastapi.Depends(ProjectListFiltersRequest),
) -> ProjectListResponse:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        params = {
            "session": session,
            "query_text": filters.query_text,
            "owner_id": filters.owner_id,
            "user_id": filters.user_id,
            "startline_le": filters.startline_le,
            "startline_ge": filters.startline_ge,
            "deadline_le": filters.deadline_le,
            "deadline_ge": filters.deadline_ge,
            "statuses": filters.status,
            "position_skill_ids": filters.position_skill_ids,
            "position_specialization_ids": filters.position_specialization_ids,
            "participant_user_ids": filters.participant_user_ids,
        }
        projects_db = await database_service.get_projects(
            page=pagination.page,
            per_page=pagination.per_page,
            **params,
        )
        total_projects = await database_service.get_projects_count(**params)

    total_pages = -(total_projects // -pagination.per_page)
    projects = [ProjectResponse.model_validate(project_db) for project_db in projects_db]

    return ProjectListResponse(
        data=projects,
        page=pagination.page,
        per_page=pagination.per_page,
        total_items=total_projects,
        total_pages=total_pages,
    )


async def get_project(
    project: Project = fastapi.Depends(get_path_project),
) -> ProjectResponse:
    return ProjectResponse.model_validate(project)


async def history(
    request: fastapi.Request,
    project: Project = fastapi.Depends(get_path_project),
    pagination: Pagination = fastapi.Depends(pagination),
) -> ProjectHistoryListResponse:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        project_history_db = await database_service.get_project_history(
            session=session,
            project_id=project.id,
            page=pagination.page,
            per_page=pagination.per_page,
        )
        total_project_history = await database_service.get_project_history_count(
            session=session, project_id=project.id
        )

    history = [ProjectHistoryResponse.model_validate(event) for event in project_history_db]
    total_pages = -(total_project_history // -pagination.per_page)
    return ProjectHistoryListResponse(
        data=history,
        page=pagination.page,
        per_page=pagination.per_page,
        total_items=total_project_history,
        total_pages=total_pages,
    )


async def partial_update_project(
    request: fastapi.Request,
    project: Project = fastapi.Depends(path_project_is_owner),
    data: ProjectPartialUpdateRequest = fastapi.Body(embed=False)
) -> ProjectResponse:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        project = await database_service.update_project(
            session=session,
            project=project,
            status=data.status,
        )

    return ProjectResponse.model_validate(project)


async def get_project_avatar(
        project: Project = fastapi.Depends(get_path_project),
) -> FileResponse:
    if project.avatar is None:
        return None

    return FileResponse(project.avatar)


async def upload_project_avatar(
        request: fastapi.Request,
        project: Project = fastapi.Depends(path_project_is_owner),
        avatar: fastapi.UploadFile = fastapi.File(...),
) -> ProjectResponse:

    database_service: database.Service = request.app.service.database
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
        database_service: database.Service = request.app.service.database
        original_avatar_file_path = project.avatar
        async with database_service.transaction() as session:
            project = await database_service.update_project(
                session=session,
                project=project,
                avatar=None,
            )

        await aiofiles.os.remove(original_avatar_file_path)

    return ProjectResponse.model_validate(project)
