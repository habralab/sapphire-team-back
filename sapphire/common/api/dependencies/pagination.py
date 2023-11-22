from typing import Any, Type
from fastapi import Query
from pydantic import BaseModel, conint

from sapphire.common.utils.empty import Empty


class OffsetPagination(BaseModel):
    page: int
    per_page: int


class CursorPagination(BaseModel):
    cursor: Any | Type[Empty] = Empty
    per_page: int


async def offset_pagination(
        page: conint(ge=1) = Query(1, description="Page number"),
        per_page: conint(ge=1) = Query(10, description="Number of items per page"),
) -> OffsetPagination:

    return OffsetPagination(page=page, per_page=per_page)


async def cursor_pagination(
        cursor: Any | None = Query(None, description="Cursor"),
        per_page: conint(ge=1) = Query(10, description="Number of items per page"),
) -> OffsetPagination:

    return CursorPagination(cursor=cursor if cursor else Empty, per_page=per_page)
