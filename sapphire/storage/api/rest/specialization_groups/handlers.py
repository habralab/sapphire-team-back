import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.storage.api.schemas.specializations import SpecializationGroupResponse
from sapphire.storage.database.service import StorageDatabaseService

from .schemas import SpecializationGroupListResponse, SpecializationGroupsFilterRequest


async def get_specialization_groups(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    filters: SpecializationGroupsFilterRequest = fastapi.Depends(SpecializationGroupsFilterRequest),
) -> SpecializationGroupListResponse:

    database_service: StorageDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        paginated_specialization_groups = await database_service.get_specialization_groups(
            session=session,
            cursor=pagination.cursor,
            per_page=pagination.per_page,
            **filters.model_dump(),
        )

    next_cursor = None
    if paginated_specialization_groups:
        next_cursor = paginated_specialization_groups[-1].created_at

    specialization_groups = [
        SpecializationGroupResponse.model_validate(s) for s in paginated_specialization_groups
    ]

    return SpecializationGroupListResponse(
        data=specialization_groups, next_cursor=next_cursor, per_page=pagination.per_page
    )
