import uuid
from typing import Type

from pydantic import BaseModel, ConfigDict, NaiveDatetime

from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.common.utils.empty import Empty
from sapphire.projects.database.models import ProjectStatusEnum


class PositionListFiltersRequest(BaseModel):
    project_id: uuid.UUID | Type[Empty] = Empty
    is_closed: bool | Type[Empty] = Empty
    specialization_ids: list[uuid.UUID] | Type[Empty] = Empty
    skill_ids: list[uuid.UUID] | Type[Empty] = Empty
    project_query_text: str | Type[Empty] = Empty
    project_startline_ge: NaiveDatetime | Type[Empty] = Empty
    project_startline_le: NaiveDatetime | Type[Empty] = Empty
    project_deadline_ge: NaiveDatetime | Type[Empty] = Empty
    project_deadline_le: NaiveDatetime | Type[Empty] = Empty
    project_status: ProjectStatusEnum | Type[Empty] = Empty


class PositionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    closed_at: NaiveDatetime | None
    created_at: NaiveDatetime
    updated_at: NaiveDatetime
    specialization_id: uuid.UUID


class PositionListResponse(PaginatedResponse):
    data: list[PositionResponse]


class CreatePositionRequest(BaseModel):
    project_id: uuid.UUID
    specialization_id: uuid.UUID
