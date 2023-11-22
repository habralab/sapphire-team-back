import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.storage.api.rest.skills.schemas import (
    SkillListResponse,
    SkillResponse,
    SkillsFiltersRequest,
)
from sapphire.storage.database.service import StorageDatabaseService


async def get_skills(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    filters: SkillsFiltersRequest = fastapi.Depends(SkillsFiltersRequest),
) -> SkillListResponse:
    database_service: StorageDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        paginated_skills = await database_service.get_skills(
            session=session,
            query_text=filters.query_text,
            skill_ids=filters.id,
            cursor=pagination.cursor,
            per_page=pagination.per_page,
        )

    next_cursor = None
    if paginated_skills:
        next_cursor = paginated_skills[-1].created_at

    skills = [SkillResponse.model_validate(s) for s in paginated_skills]

    return SkillListResponse(data=skills, next_cursor=next_cursor, per_page=pagination.per_page)
