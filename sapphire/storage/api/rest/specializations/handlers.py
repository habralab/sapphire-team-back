import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.storage.api.rest.specializations.schemas import (
    SpecializationFiltersRequest,
    SpecializationListResponse,
)
from sapphire.storage.api.schemas.specializations import SpecializationResponse
from sapphire.storage.database.service import StorageDatabaseService


async def get_specializations(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    filters: SpecializationFiltersRequest = fastapi.Depends(SpecializationFiltersRequest),
) -> SpecializationListResponse:

    database_service: StorageDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        paginated_specializations = await database_service.get_specializations(
            session=session,
            cursor=pagination.cursor,
            per_page=pagination.per_page,
            **filters.model_dump(),
        )

    next_cursor = None
    if paginated_specializations:
        next_cursor = paginated_specializations[-1].created_at

    specializations = [
            SpecializationResponse.model_validate(s) for s in paginated_specializations
        ]

    return SpecializationListResponse(
        data=specializations, next_cursor=next_cursor, per_page=pagination.per_page
    )
