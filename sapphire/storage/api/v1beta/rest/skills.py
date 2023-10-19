import fastapi

from sapphire.common.api.dependencies.pagination import pagination
from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.storage.api.schemas.skills import SkillResponse
from sapphire.storage.database.service import StorageDatabaseService


async def get_skills(
    request: fastapi.Request,
    response: fastapi.Response,
    pagination: dict = fastapi.Depends(pagination),
    ) -> PaginatedResponse:

    database_service: StorageDatabaseService = request.app.service.database
    page = pagination.page
    per_page = pagination.per_page

    async with database_service.transaction() as session:
        paginated_skills = await database_service.get_skills(
            session=session, page=page, per_page=per_page,
        )

    skills = [
            SkillResponse.model_validate(s) for s in paginated_skills
        ]

    return PaginatedResponse(
        data=skills,
        page=page,
        per_page=per_page,
    )
