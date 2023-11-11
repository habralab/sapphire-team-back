from pydantic import BaseModel, NonNegativeInt, PositiveInt


class PaginatedResponse(BaseModel):
    data: list
    page: PositiveInt
    per_page: PositiveInt
    total_pages: NonNegativeInt | None
    total_items: NonNegativeInt | None
