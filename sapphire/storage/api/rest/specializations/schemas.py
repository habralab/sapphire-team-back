import uuid
from typing import Type

from pydantic import BaseModel

from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.common.utils.empty import Empty


class SpecializationFiltersRequest(BaseModel):
    query_text: str | Type[Empty] = Empty
    is_other: bool | Type[Empty] = Empty
    group_id: uuid.UUID | Type[Empty] = Empty


class SpecializationListResponce(PaginatedResponse):
    data: list[SpecializationFiltersRequest]
