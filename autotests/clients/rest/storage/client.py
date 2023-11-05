from typing import Type

from autotests.clients.rest.base_client import BaseRestClient
from autotests.utils import Empty

from .models import (
    HealthResponse,
    SkillListResponse,
    SpecializationGroupListResponse,
    SpecializationListResponse,
)


class StorageRestClient(BaseRestClient):
    async def get_health(self) -> HealthResponse:
        path = "/health"

        return await self.rest_get(path=path, response_model=HealthResponse)

    async def get_specialization_groups(self) -> SpecializationGroupListResponse:
        path = "/api/rest/spec-groups/"

        return await self.rest_get(path=path, response_model=SpecializationGroupListResponse)

    async def get_specializations(self) -> SpecializationListResponse:
        path = "/api/rest/specializations/"

        return await self.rest_get(path=path, response_model=SpecializationListResponse)

    async def get_skills(self, query_text: str | Type[Empty] = Empty) -> SkillListResponse:
        path = "/api/rest/skills/"
        params = {"query_text": query_text}
        params = {key: value for key, value in params.items() if value is not Empty}

        return await self.rest_get(path=path, response_model=SkillListResponse, params=params)
