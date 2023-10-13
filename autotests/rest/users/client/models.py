from typing import Literal

from pydantic import BaseModel, constr


class HealthResponse(BaseModel):
    name: Literal["users"]
    version: constr(pattern=r"^\d+\.\d+\.\d+$")
