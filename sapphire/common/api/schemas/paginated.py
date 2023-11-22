from datetime import datetime
from typing import Any

from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    data: list[Any]
    next_cursor: datetime | None
    per_page: int
