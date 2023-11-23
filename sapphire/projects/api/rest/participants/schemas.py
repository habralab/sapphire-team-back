import uuid

from pydantic import BaseModel

from sapphire.common.api.schemas.paginated import PaginatedResponse
from sapphire.projects.api.rest.projects.schemas import ParticipantResponse
from sapphire.projects.database.models import ParticipantStatusEnum


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
    status: ParticipantStatusEnum
    created_at_le: NaiveDatetime | Type[Empty] = Empty
    created_at_ge: NaiveDatetime | Type[Empty] = Empty
    joined_at_le: NaiveDatetime | Type[Empty] = Empty
    joined_at_ge: NaiveDatetime | Type[Empty] = Empty

    updated_at_le: NaiveDatetime | Type[Empty] = Empty
    updated_at_ge: NaiveDatetime | Type[Empty] = Empty
