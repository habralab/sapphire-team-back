from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar('T')

class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total_pages: Optional[int] = None
    total_items: Optional[int] = None

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    meta: PaginationMeta