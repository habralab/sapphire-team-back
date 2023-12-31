from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt


class UserStatisticResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ownership_projects_count: NonNegativeInt
    participant_projects_count: NonNegativeInt
    rate: Annotated[float, Field(ge=1, le=5)]
