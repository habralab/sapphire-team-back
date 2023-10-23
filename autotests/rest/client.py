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
    ) -> ResponseModel:
        request_data = None if data is None else data.model_dump()
        response = await self.request(method=method, url=path, json=request_data)

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
    ) -> ResponseModel:
        return await self.rest_request(method="POST", path=path, response_model=response_model,
                                       data=data)

    async def rest_delete(self, path: str, response_model: Type[ResponseModel]) -> ResponseModel:
        return await self.rest_request(method="DELETE", path=path, response_model=response_model)
