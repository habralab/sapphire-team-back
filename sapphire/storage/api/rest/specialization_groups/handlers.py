import fastapi

from sapphire.common.api.dependencies.pagination import pagination
from sapphire.storage.api.schemas.specializations import SpecializationGroupResponse
from sapphire.storage.database.service import StorageDatabaseService

from .schemas import SpecializationGroupListResponse, SpecializationGroupsFilterRequest


async def get_specialization_groups(
    request: fastapi.Request,
    pagination: dict = fastapi.Depends(pagination),
    filters: SpecializationGroupsFilterRequest = fastapi.Depends(SpecializationGroupsFilterRequest),
) -> SpecializationGroupListResponse:

    database_service: StorageDatabaseService = request.app.service.database
    page = pagination.page
    per_page = pagination.per_page

    async with database_service.transaction() as session:
        paginated_specialization_groups = await database_service.get_specialization_groups(
            session=session, page=page, per_page=per_page, **filters.model_dump()
        )

        total_specialization_groups = await database_service.get_specialization_groups_count(
            session=session, **filters.model_dump()
        )

    total_pages = -(total_specialization_groups // -per_page)
    specialization_groups = [
        SpecializationGroupResponse.model_validate(s) for s in paginated_specialization_groups
    ]

    return SpecializationGroupListResponse(
        data=specialization_groups,
        page=page,
        per_page=per_page,
        total_items=total_specialization_groups,
        total_pages=total_pages,
    )
