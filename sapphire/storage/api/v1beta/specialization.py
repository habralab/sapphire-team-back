from typing import Annotated, Optional

import fastapi

from sapphire.common.api.dependancies.pagination import pagination
from sapphire.storage.database.service import StorageDatabaseService
from sapphire.common.api.schemas.paginated import PaginatedResponse, PaginationMeta

router = fastapi.APIRouter()


@router.get("/specs_paginated")
async def specializations(
    request: fastapi.Request,
    response: fastapi.Response,
    pagination: Annotated[dict, fastapi.Depends(pagination)],
    ) -> fastapi.Response:

    database_service: StorageDatabaseService = request.app.service.database
    page = int(request.query_params.get("page"))
    per_page = int(request.query_params.get("per_page"))

    async with database_service.transaction() as session:
        paginated_specializations = await database_service.get_specializations_paginated(
            session=session, page=page, per_page=per_page,
        )

    specializations = [fastapi.encoders.jsonable_encoder(s) for s in paginated_specializations]


    return PaginatedResponse(
        data=specializations,
        meta=PaginationMeta(
            page=page, per_page=per_page
        ),
    )
