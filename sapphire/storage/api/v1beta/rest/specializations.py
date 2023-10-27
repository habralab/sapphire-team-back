import fastapi

from sapphire.common.api.dependencies.pagination import pagination
from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.storage.api.schemas.specializations import (
    SpecializationGroupResponse,
    SpecializationResponse,
)
from sapphire.storage.database.service import StorageDatabaseService


async def get_specializations(
    request: fastapi.Request,
    pagination: dict = fastapi.Depends(pagination),
) -> PaginatedResponse:

    database_service: StorageDatabaseService = request.app.service.database
    page = pagination.page
    per_page = pagination.per_page

    async with database_service.transaction() as session:
        paginated_specializations = await database_service.get_specializations(
            session=session, page=page, per_page=per_page,
        )

    specializations = [
            SpecializationResponse.model_validate(s) for s in paginated_specializations
        ]

    return PaginatedResponse(
        data=specializations,
        page=page,
        per_page=per_page,
    )


async def get_specialization_groups(
    request: fastapi.Request,
    pagination: dict = fastapi.Depends(pagination),
) -> PaginatedResponse:

    database_service: StorageDatabaseService = request.app.service.database
    page = pagination.page
    per_page = pagination.per_page

    async with database_service.transaction() as session:
        paginated_specialization_groups = await database_service.get_specialization_groups(
            session=session, page=page, per_page=per_page,
        )

    specialization_groups = [
            SpecializationGroupResponse.model_validate(s) for s in paginated_specialization_groups
        ]

    return PaginatedResponse(
        data=specialization_groups,
        page=page,
        per_page=per_page,
    )