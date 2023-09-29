from .base import BaseResponse


class HealthResponse(BaseResponse):
    version: str
    name: str
