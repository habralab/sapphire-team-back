from typing import Optional

import fastapi

from sapphire.storage.database.models import Specialization
from sapphire.storage.database.service import StorageDatabaseService

router = fastapi.APIRouter()


@router.get("/specializations")
async def specializations(
    request: fastapi.Request,
    response: fastapi.Response,
    page: Optional[int] = fastapi.Query(1, ge=1), per_page: Optional[int] = fastapi.Query(10, ge=1),
    ) -> fastapi.Response:
    database_service: StorageDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        paginated_specializations = await database_service.get_specializations_paginated(
            session=session, page=page, per_page=per_page,
        )

    specialization_objects = []
    for specialization in paginated_specializations.items:
        specialization_object = fastapi.encoders.jsonable_encoder(specialization)
        specialization_objects.append(specialization_object)

    response.body = fastapi.encoders.jsonable_encoder({
        "data": specialization_objects,
        "page": page, "per_page": per_page
        })
    response.headers["X-Total-Pages"] = str(paginated_specializations.total_pages)
    response.headers["X-Total-Count"] = str(paginated_specializations.total)

    return response
