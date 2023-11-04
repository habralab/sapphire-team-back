import fastapi

from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.storage.api.rest.dependencies import Pagination, pagination
from sapphire.storage.api.rest.skills.schemas import SkillResponse, SkillsFiltersRequest
from sapphire.storage.database.service import StorageDatabaseService


async def get_skills(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    filters: SkillsFiltersRequest = fastapi.Depends(SkillsFiltersRequest),
) -> PaginatedResponse:
    database_service: StorageDatabaseService = request.app.service.database
    page = pagination.page
    per_page = pagination.per_page

    async with database_service.transaction() as session:
        paginated_skills = await database_service.get_skills(
            session=session,
            query_text=filters.query_text,
            skill_ids=filters.id,
            page=page,
            per_page=per_page,
        )

    skills = [SkillResponse.model_validate(s) for s in paginated_skills]

    return PaginatedResponse(
        data=skills,
        page=page,
        per_page=per_page,
    )
