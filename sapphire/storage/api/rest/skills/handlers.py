import fastapi

from sapphire.storage import database
from sapphire.storage.api.rest.dependencies import Pagination, pagination
from sapphire.storage.api.rest.skills.schemas import (
    SkillListResponse,
    SkillResponse,
    SkillsFiltersRequest,
)


async def get_skills(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    filters: SkillsFiltersRequest = fastapi.Depends(SkillsFiltersRequest),
) -> SkillListResponse:
    database_service: database.Service = request.app.service.database
    page = pagination.page
    per_page = pagination.per_page

    async with database_service.transaction() as session:
        params = {
            "session": session,
            "query_text": filters.query_text,
            "skill_ids": filters.id,
            "exclude_skill_ids": filters.exclude_id,
        }
        skills = await database_service.get_skills(**params, page=page, per_page=per_page)
        total_items = await database_service.get_skills_count(**params)

    total_pages = -(total_items // -per_page)
    data = [SkillResponse.model_validate(s) for s in skills]

    return SkillListResponse(
        data=data,
        page=page,
        per_page=per_page,
        total_items=total_items,
        total_pages=total_pages,
    )
