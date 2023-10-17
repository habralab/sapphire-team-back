from fastapi import Query
from pydantic import conint

from ..schemas.paginated import PaginationModel


async def pagination(

        page: conint(ge=1) = Query(1, description="Page number"),
        per_page: conint(ge=1) = Query(10, description="Number of items per page"),

    ) -> PaginationModel:

    return PaginationModel(page=page, per_page=per_page)
