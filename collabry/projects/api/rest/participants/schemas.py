import uuid
from typing import Type

from pydantic import AwareDatetime, BaseModel

from collabry.common.api.schemas.paginated import PaginatedResponse
from collabry.common.utils.empty import Empty
from collabry.database.models import ParticipantStatusEnum
from collabry.projects.api.rest.projects.schemas import ParticipantResponse


class CreateParticipantRequest(BaseModel):
    position_id: uuid.UUID


class UpdateParticipantRequest(BaseModel):
    status: ParticipantStatusEnum


class ParticipantListResponse(PaginatedResponse):
    data: list[ParticipantResponse]


class ParticipantListFiltersRequest(BaseModel):
    user_id: uuid.UUID | Type[Empty] = Empty
    position_id: uuid.UUID | Type[Empty] = Empty
    project_id: uuid.UUID | Type[Empty] = Empty
    status: ParticipantStatusEnum | Type[Empty] = Empty
    created_at_le: AwareDatetime | Type[Empty] = Empty
    created_at_ge: AwareDatetime | Type[Empty] = Empty
    joined_at_le: AwareDatetime | Type[Empty] = Empty
    joined_at_ge: AwareDatetime | Type[Empty] = Empty
    updated_at_le: AwareDatetime | Type[Empty] = Empty
    updated_at_ge: AwareDatetime | Type[Empty] = Empty
