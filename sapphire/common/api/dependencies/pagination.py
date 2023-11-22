from datetime import datetime
from typing import Type

from fastapi import Query
from pydantic import BaseModel, conint

from sapphire.common.utils.empty import Empty


class Pagination(BaseModel):
    cursor: datetime | Type[Empty] = Empty
    per_page: int


async def pagination(
        cursor: datetime | None = Query(None, description="Cursor"),
        per_page: conint(ge=1) = Query(10, description="Number of items per page"),
) -> Pagination:

    return Pagination(cursor=cursor if cursor else Empty, per_page=per_page)
