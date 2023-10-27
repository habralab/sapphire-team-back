import math

import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.projects.api.rest.projects.dependencies import get_path_project, path_project_is_owner
from sapphire.projects.database.models import Position, Project
from sapphire.projects.database.service import ProjectsDatabaseService

from .dependencies import get_path_position
from .schemas import ProjectPositionResponse, ProjectPositionsResponse


async def get_project_positions(
        request: fastapi.Request,
        project: Project = fastapi.Depends(get_path_project),
        pagination: Pagination = fastapi.Depends(pagination),
) -> ProjectPositionsResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        positions = await database_service.get_project_positions(
            session=session,
            project_id=project.id,
        )

    total_items = len(positions)
    total_pages = int(math.ceil(total_items / pagination.per_page))
    offset = (pagination.page - 1) * pagination.per_page
    positions = positions[offset:offset + pagination.per_page]
    data = [ProjectPositionResponse.model_validate(position) for position in positions]

    return ProjectPositionsResponse(
        data=data,
        total_items=total_items,
        total_pages=total_pages,
        page=pagination.page,
        per_page=pagination.per_page,
    )


async def create_project_position(
        request: fastapi.Request,
        project: Project = fastapi.Depends(path_project_is_owner),
) -> ProjectPositionResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_position = await database_service.create_project_position(
            session=session,
            project=project,
        )

    return ProjectPositionResponse.model_validate(db_position)


async def remove_project_position(
        request: fastapi.Request,
        project: Project = fastapi.Depends(path_project_is_owner),
        position: Position = fastapi.Depends(get_path_position),
) -> ProjectPositionResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        position = await database_service.remove_project_position(
            session=session,
            position=position,
        )

    return ProjectPositionResponse.model_validate(position)
