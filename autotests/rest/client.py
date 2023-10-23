import io
from typing import Any, Type, TypeVar

import httpx
from facet import ServiceMixin
from pydantic import BaseModel

ResponseModel = TypeVar("ResponseModel")


class ResponseException(Exception):
    def __init__(self, status_code: int, body: bytes):
        self.status_code = status_code
        self.body = body

        super().__init__(f"Response exception [{status_code}]: {body[:20]}")


class BaseRestClient(httpx.AsyncClient, ServiceMixin):
    def __init__(
            self,
            base_url: str = "",
            headers: dict[str, Any] | None = None,
            verify: bool = True,
    ):
        super().__init__(base_url=base_url, headers=headers, verify=verify)

    async def start(self):
        await self.__aenter__()  # pylint: disable=unnecessary-dunder-call

    async def stop(self):
        await self.__aexit__()  # pylint: disable=unnecessary-dunder-call

    async def rest_request(
            self,
            method: str,
            path: str,
            response_model: Type[ResponseModel],
            data: BaseModel | None = None,
            files: dict[str, io.BytesIO] | None = None,
            headers: dict[str, Any] | None = None,
    ) -> ResponseModel:
        headers = headers or {}
        request_data = None
        if isinstance(data, BaseModel):
            request_data = data.model_dump_json()
            headers["Content-Type"] = "application/json"

        response = await self.request(method=method, url=path, content=request_data, files=files,
                                      headers=headers)

        if response.status_code // 100 != 2:
            raise ResponseException(status_code=response.status_code, body=response.read())

        return response_model.model_validate(response.json())

    async def rest_get(self, path: str, response_model: Type[ResponseModel]) -> ResponseModel:
        return await self.rest_request(method="GET", path=path, response_model=response_model)

    async def rest_post(
            self,
            path: str,
            response_model: Type[ResponseModel],
            data: BaseModel | None = None,
            files: dict[str, io.BytesIO] | None = None,
    ) -> ResponseModel:
        return await self.rest_request(method="POST", path=path, response_model=response_model,
                                       data=data, files=files)

    async def rest_delete(self, path: str, response_model: Type[ResponseModel]) -> ResponseModel:
        return await self.rest_request(method="DELETE", path=path, response_model=response_model)
