import fastapi

from collabry.common.api.dependencies.pagination import Pagination, pagination
from collabry.storage import database
from collabry.storage.api.rest.specializations.schemas import (
    SpecializationFiltersRequest,
    SpecializationListResponse,
)
from collabry.storage.api.schemas.specializations import SpecializationResponse


async def get_specializations(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    filters: SpecializationFiltersRequest = fastapi.Depends(SpecializationFiltersRequest),
) -> SpecializationListResponse:

    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        params = {
            "session": session,
            "query": filters.query,
            "group_id": filters.group_id,
            "specialization_ids": filters.id,
            "exclude_specialization_ids": filters.exclude_id,
        }
        paginated_specializations = await database_service.get_specializations(
            **params,
            page=pagination.page,
            per_page=pagination.per_page,
        )
        total_specializations = await database_service.get_specializations_count(
            **params,
        )

    total_pages = -(total_specializations // -pagination.per_page)
    specializations = [
        SpecializationResponse.model_validate(s) for s in paginated_specializations
    ]

    return SpecializationListResponse(
        data=specializations,
        page=pagination.page,
        per_page=pagination.per_page,
        total_items=total_specializations,
        total_pages=total_pages,
    )
