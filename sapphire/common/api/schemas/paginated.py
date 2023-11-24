from typing import Any

from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    data: list[Any]
    page: int
    per_page: int
    total_pages: int
    total_items: int
