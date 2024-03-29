import uuid

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class CreateReviewRequest(BaseModel):
    project_id: uuid.UUID
    user_id: uuid.UUID
    rate: int = Field(ge=1, le=5)
    text: str


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    from_user_id: uuid.UUID
    to_user_id: uuid.UUID
    rate: int = Field(ge=1, le=5)
    text: str
    created_at: AwareDatetime
    updated_at: AwareDatetime
