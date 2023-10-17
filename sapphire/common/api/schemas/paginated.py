from typing import Any

from pydantic import BaseModel


class PaginationModel(BaseModel):
    page: int
    per_page: int


class PaginatedResponse(PaginationModel):
    data: list[Any]
    total_pages: int | None = None
    total_items: int | None = None
