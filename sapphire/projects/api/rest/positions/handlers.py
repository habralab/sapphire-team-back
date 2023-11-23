import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.api.exceptions import HTTPForbidden, HTTPNotFound
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.projects.database.models import Position
from sapphire.projects.database.service import ProjectsDatabaseService

from .dependencies import get_path_position, path_position_is_owner
from .schemas import (
    CreatePositionRequest,
    PositionListFiltersRequest,
    PositionListResponse,
    PositionResponse,
)


async def get_positions(
        request: fastapi.Request,
        filters: PositionListFiltersRequest = fastapi.Depends(PositionListFiltersRequest),
        pagination: Pagination = fastapi.Depends(pagination),
) -> PositionListResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        positions = await database_service.get_positions(
            session=session,
            page=pagination.page,
            per_page=pagination.per_page,
            **filters.model_dump(),
        )

    data = [PositionResponse.from_db_model(position) for position in positions]

    return PositionListResponse(
        data=data,
        page=pagination.page,
        per_page=pagination.per_page,
    )


async def create_position(
        request: fastapi.Request,
        jwt_data: JWTData = fastapi.Depends(is_auth),
        data: CreatePositionRequest = fastapi.Body(embed=False),
) -> PositionResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_project = await database_service.get_project(session=session, project_id=data.project_id)

    if db_project is None:
        raise HTTPNotFound()
    if db_project.owner_id != jwt_data.user_id:
        raise HTTPForbidden()

    async with database_service.transaction() as session:
        db_position = await database_service.create_position(
            session=session,
            project=db_project,
            specialization_id=data.specialization_id,
        )

    return PositionResponse.from_db_model(db_position)


async def get_position(
        position: Position = fastapi.Depends(get_path_position),
):
    return PositionResponse.from_db_model(position)


async def remove_position(
        request: fastapi.Request,
        position: Position = fastapi.Depends(path_position_is_owner),
) -> PositionResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        position = await database_service.remove_position(
            session=session,
            position=position,
        )

    return PositionResponse.from_db_model(position)
