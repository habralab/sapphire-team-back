from pydantic import BaseModel, NaiveDatetime, PositiveInt


class PaginatedResponse(BaseModel):
    data: list
    next_cursor: NaiveDatetime | None
    per_page: PositiveInt
