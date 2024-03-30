import fastapi

from collabry.common.api.dependencies.pagination import Pagination, pagination
from collabry.storage import database
from collabry.storage.api.schemas.specializations import SpecializationGroupResponse

from .schemas import SpecializationGroupListResponse, SpecializationGroupsFilterRequest


async def get_specialization_groups(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    filters: SpecializationGroupsFilterRequest = fastapi.Depends(SpecializationGroupsFilterRequest),
) -> SpecializationGroupListResponse:

    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        params = {
            "session": session,
            "query": filters.query,
            "group_ids": filters.id,
            "exclude_group_ids": filters.exclude_id,
        }
        paginated_specialization_groups = await database_service.get_specialization_groups(
            **params,
            page=pagination.page,
            per_page=pagination.per_page,
        )

        total_specialization_groups = await database_service.get_specialization_groups_count(
            **params,
        )

    total_pages = -(total_specialization_groups // -pagination.per_page)
    specialization_groups = [
        SpecializationGroupResponse.model_validate(s) for s in paginated_specialization_groups
    ]

    return SpecializationGroupListResponse(
        data=specialization_groups,
        page=pagination.page,
        per_page=pagination.per_page,
        total_items=total_specialization_groups,
        total_pages=total_pages,
    )
