from pydantic import BaseModel, ConfigDict, NonNegativeInt, confloat


class UserStatisticResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ownership_projects_count: NonNegativeInt
    participant_projects_count: NonNegativeInt
    rate: confloat(ge=1, le=5)
