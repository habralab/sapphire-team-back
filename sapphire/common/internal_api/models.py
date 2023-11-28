from pydantic import BaseModel, NonNegativeInt, PositiveInt


class ListBaseRequest(BaseModel):
    page: PositiveInt = 1
    per_page: PositiveInt = 10


class ListBaseResponse(BaseModel):
    data: list
    page: PositiveInt
    per_page: PositiveInt
    total_items: NonNegativeInt
    total_pages: NonNegativeInt
