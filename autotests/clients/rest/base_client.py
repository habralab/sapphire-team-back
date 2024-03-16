import io
import json
from typing import Any, Type, TypeVar

import httpx
from facet import ServiceMixin
from pydantic import BaseModel

from .exceptions import ResponseException

ResponseModel = TypeVar("ResponseModel")


class BaseRestClient(httpx.AsyncClient, ServiceMixin):
    def __init__(
            self,
            base_url: str = "",
            headers: dict[str, Any] | None = None,
            timeout: float = 30,
            verify: bool = True,
    ):
        super().__init__(base_url=base_url, headers=headers, verify=verify, timeout=timeout)

    async def start(self):
        await self.__aenter__()  # pylint: disable=unnecessary-dunder-call

    async def stop(self):
        await self.__aexit__()  # pylint: disable=unnecessary-dunder-call

    async def request(self, *args, **kwargs):
        response = await super().request(*args, **kwargs)
        self.cookies.clear()
        return response

    async def rest_request(
            self,
            method: str,
            path: str,
            response_model: Type[ResponseModel],
            data: BaseModel | dict[str, Any] | None = None,
            params: BaseModel | dict[str, Any] | None = None,
            files: dict[str, io.BytesIO] | None = None,
            headers: dict[str, Any] | None = None,
    ) -> ResponseModel:
        headers = headers or {}
        request_data = None
        request_params = None
        if isinstance(data, BaseModel):
            request_data = data.model_dump_json()
            headers["Content-Type"] = "application/json"
        elif isinstance(data, dict):
            request_data = json.dumps(data)
            headers["Content-Type"] = "application/json"
        if isinstance(params, BaseModel):
            request_params = params.model_dump()
        elif isinstance(params, dict):
            request_params = params

        response = await self.request(method=method, url=path, content=request_data, files=files,
                                      params=request_params, headers=headers)

        if response.status_code // 100 != 2:
            raise ResponseException(status_code=response.status_code, body=response.read())

        return response_model.model_validate(response.json())

    async def rest_get(
            self,
            path: str,
            response_model: Type[ResponseModel],
            params: BaseModel | dict[str, Any] | None = None,
    ) -> ResponseModel:
        return await self.rest_request(
            method="GET",
            path=path,
            params=params,
            response_model=response_model,
        )

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

    async def rest_patch(
            self,
            path: str,
            response_model: Type[ResponseModel],
            data: BaseModel | None = None,
            files: dict[str, io.BytesIO] | None = None,
    ) -> ResponseModel:
        return await self.rest_request(method="PATCH", path=path, response_model=response_model,
                                       data=data, files=files)
