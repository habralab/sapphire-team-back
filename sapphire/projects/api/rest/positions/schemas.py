import uuid
from typing import Type

from pydantic import BaseModel, ConfigDict, NaiveDatetime

from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.common.utils.empty import Empty
from sapphire.projects.api.rest.schemas import ProjectResponse
from sapphire.projects.database.models import Position, ProjectStatusEnum


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
    project: ProjectResponse
    specialization_id: uuid.UUID
    skills: list[uuid.UUID]
    closed_at: NaiveDatetime | None
    created_at: NaiveDatetime
    updated_at: NaiveDatetime

    @classmethod
    def from_db_model(cls, instance: Position):
        return cls(
            id=instance.id,
            project=ProjectResponse.model_validate(instance.project),
            specialization_id=instance.specialization_id,
            skills=[skill.skill_id for skill in instance.skills],
            closed_at=instance.closed_at,
            created_at=instance.created_at,
            updated_at=instance.updated_at,
        )


class PositionListResponse(PaginatedResponse):
    data: list[PositionResponse]


class CreatePositionRequest(BaseModel):
    project_id: uuid.UUID
    specialization_id: uuid.UUID
