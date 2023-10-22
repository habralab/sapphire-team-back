from fastapi import Query
from pydantic import BaseModel, conint


class Pagination(BaseModel):
    page: int
    per_page: int


async def pagination(
        page: conint(ge=1) = Query(1, description="Page number"),
        per_page: conint(ge=1) = Query(10, description="Number of items per page"),
) -> Pagination:

    return Pagination(page=page, per_page=per_page)
