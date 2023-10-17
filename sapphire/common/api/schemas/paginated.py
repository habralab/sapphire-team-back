from typing import Any

from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    data: list[Any]
    page: int
    per_page: int
    total_pages: int | None = None
    total_items: int | None = None
