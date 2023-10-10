from typing import Optional

import fastapi

from sapphire.storage.database.service import StorageDatabaseService

router = fastapi.APIRouter()


@router.get("/specializations")
async def specializations(
    request: fastapi.Request,
    page: Optional[int] = fastapi.Query(1, ge=1), per_page: Optional[int] = fastapi.Query(10, ge=1),
    ) -> fastapi.Response:
    database_service: StorageDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        specializations = await session.query(Specialization).order_by(Specialization.created_at.desc())

    paginated_specializations = specializations.paginate(page, per_page, error_out=False)

    specialization_objects = []
    for specialization in paginated_specializations.items:
        specialization_object = jsonable_encoder(specialization)
        specialization_objects.append(specialization_object)
    
    response = Response(jsonable_encoder({"data": specialization_objects}))
    response.headers["X-Total-Pages"] = str(paginated_specializations.total_pages)
    response.headers["X-Total-Count"] = str(paginated_specializations.total)

    return response