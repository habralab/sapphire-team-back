from pydantic import BaseModel

from .enums import ResponseStatus


class BaseResponse(BaseModel):
    status: ResponseStatus


class OKResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.OK
