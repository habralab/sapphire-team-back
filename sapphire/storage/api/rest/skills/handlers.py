import fastapi

from sapphire.storage.api.rest.dependencies import Pagination, pagination
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
    page = pagination.page
    per_page = pagination.per_page

    async with database_service.transaction() as session:
        skills = await database_service.get_skills(
            session=session,
            query_text=filters.query_text,
            skill_ids=filters.id,
            page=page,
            per_page=per_page,
        )
        total_items = await database_service.get_skills_count(
            session=session,
            query_text=filters.query_text,
            skill_ids=filters.id,
        )

    total_pages = -(total_items // -per_page)
    data = [SkillResponse.model_validate(s) for s in skills]

    return SkillListResponse(
        data=data,
        page=page,
        per_page=per_page,
        total_items=total_items,
        total_pages=total_pages,
    )
