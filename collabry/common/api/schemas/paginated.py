from typing import Any

from pydantic import BaseModel, NonNegativeInt, PositiveInt


class PaginatedResponse(BaseModel):
    data: list[Any]
    page: PositiveInt
    per_page: PositiveInt
    total_pages: NonNegativeInt
    total_items: NonNegativeInt
