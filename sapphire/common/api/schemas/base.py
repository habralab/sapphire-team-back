from pydantic import BaseModel

from .enums import ResponseStatus, ServiceName


class OKResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.OK


class HealthResponse(OKResponse):
    version: str
    name: ServiceName
