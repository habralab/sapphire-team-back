import fastapi
from pydantic import BaseModel, PositiveInt


class Pagination(BaseModel):
    page: PositiveInt = 1
    per_page: PositiveInt = 100


async def pagination(
        page: PositiveInt = fastapi.Query(1, description="Page number"),
        per_page: PositiveInt = fastapi.Query(100, description="Number of items per page"),
) -> Pagination:
    return Pagination(page=page, per_page=per_page)
