from pydantic import BaseModel
from enum import Enum


class ResponseStatus(Enum):
    OK = 'OK'
    ERROR = 'ERROR'


class ErrorResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ERROR
    message: str = ''


class OKResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.OK
