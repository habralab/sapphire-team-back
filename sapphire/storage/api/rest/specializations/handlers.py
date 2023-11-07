import fastapi

from sapphire.common.api.dependencies.pagination import pagination
from sapphire.storage.api.rest.specializations.schemas import (
    SpecializationFiltersRequest,
    SpecializationListResponse,
)
from sapphire.storage.api.schemas.specializations import SpecializationResponse
from sapphire.storage.database.service import StorageDatabaseService


async def get_specializations(
    request: fastapi.Request,
    pagination: dict = fastapi.Depends(pagination),
    filters: SpecializationFiltersRequest = fastapi.Depends(SpecializationFiltersRequest),
) -> SpecializationListResponse:

    database_service: StorageDatabaseService = request.app.service.database
    page = pagination.page
    per_page = pagination.per_page

    async with database_service.transaction() as session:
        paginated_specializations = await database_service.get_specializations(
            session=session, page=page, per_page=per_page, **filters.model_dump(),
        )

    specializations = [
            SpecializationResponse.model_validate(s) for s in paginated_specializations
        ]

    return SpecializationListResponse(
        data=specializations,
        page=page,
        per_page=per_page,
    )
