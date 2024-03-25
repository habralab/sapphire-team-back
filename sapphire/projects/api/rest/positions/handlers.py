import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.api.exceptions import HTTPForbidden, HTTPNotFound
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.database.models import Position
from sapphire.projects import database

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
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        params = {
            "session": session,
            "project_id": filters.project_id,
            "specialization_ids": filters.specialization_ids,
            "skill_ids": filters.skill_ids,
            "joined_user_id": filters.joined_user_id,
            "query": filters.query,
            "project_startline_ge": filters.project_startline_ge,
            "project_startline_le": filters.project_startline_le,
            "project_deadline_ge": filters.project_deadline_ge,
            "project_deadline_le": filters.project_deadline_le,
            "project_statuses": filters.project_status,
        }
        db_positions = await database_service.get_positions(
            **params,
            page=pagination.page,
            per_page=pagination.per_page,
        )
        total_positions = await database_service.get_positions_count(**params)

    total_pages = -(total_positions // -pagination.per_page)
    positions = [PositionResponse.from_db_model(position) for position in db_positions]

    return PositionListResponse(
        data=positions,
        page=pagination.page,
        per_page=pagination.per_page,
        total_items=total_positions,
        total_pages=total_pages,
    )


async def create_position(
        request: fastapi.Request,
        jwt_data: JWTData = fastapi.Depends(is_auth),
        data: CreatePositionRequest = fastapi.Body(embed=False),
) -> PositionResponse:
    database_service: database.Service = request.app.service.database

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
) -> PositionResponse:
    return PositionResponse.from_db_model(position)


async def remove_position(
        request: fastapi.Request,
        position: Position = fastapi.Depends(path_position_is_owner),
) -> PositionResponse:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        position = await database_service.remove_position(
            session=session,
            position=position,
        )

    return PositionResponse.from_db_model(position)
