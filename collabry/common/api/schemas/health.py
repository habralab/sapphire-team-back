from pydantic import BaseModel


class HealthResponse(BaseModel):
    version: str
    name: str
