import uuid
from typing import Type

from pydantic import BaseModel

from sapphire.common.api.schemas.paginated import OffsetPaginatedResponse
from sapphire.common.utils.empty import Empty
from sapphire.storage.api.schemas.specializations import SpecializationResponse


class SpecializationFiltersRequest(BaseModel):
    query_text: str | Type[Empty] = Empty
    group_id: uuid.UUID | Type[Empty] = Empty


class SpecializationListResponse(OffsetPaginatedResponse):
    data: list[SpecializationResponse]
