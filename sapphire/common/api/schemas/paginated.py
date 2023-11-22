from typing import Any

from pydantic import BaseModel


class OffsetPaginatedResponse(BaseModel):
    data: list[Any]
    page: int
    per_page: int
    total_pages: int | None = None
    total_items: int | None = None


class CursorPaginatedResponse(BaseModel):
    data: list[Any]
    next_cursor: Any | None
    per_page: int
