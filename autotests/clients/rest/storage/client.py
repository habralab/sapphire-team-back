import uuid
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

    async def get_specialization_groups(
        self, query_text: str | Type[Empty] = Empty
    ) -> SpecializationGroupListResponse:
        path = "/api/rest/spec-groups/"
        params = {"query_text": query_text}
        params = {key: value for key, value in params.items() if value is not Empty}

        return await self.rest_get(
            path=path, response_model=SpecializationGroupListResponse, params=params
        )

    async def get_specializations(
        self,
        query_text: str | type[Empty] = Empty,
        is_other: bool | Type[Empty] = Empty,
        group_id: uuid.UUID | Type[Empty] = Empty,
    ) -> SpecializationListResponse:
        path = "/api/rest/specializations/"
        params = {
            "query_text": query_text,
            "is_other": is_other,
            "group_id": group_id
        }
        params = {key: value for key, value in params.items() if value is not Empty}

        return await self.rest_get(
            path=path, response_model=SpecializationListResponse, params=params
        )

    async def get_skills(
            self,
            query_text: str | Type[Empty] = Empty,
            skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> SkillListResponse:
        path = "/api/rest/skills/"
        params = {"query_text": query_text, "id": skill_ids}
        params = {key: value for key, value in params.items() if value is not Empty}

        return await self.rest_get(path=path, response_model=SkillListResponse, params=params)
