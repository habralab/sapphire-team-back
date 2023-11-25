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
        params = {
            "session": session,
            "query_text": filters.query_text,
            "group_id": filters.group_id,
            "specialization_ids": filters.id,
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
