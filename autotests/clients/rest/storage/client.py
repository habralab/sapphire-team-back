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
        self,
        query: str | Type[Empty] = Empty,
        group_ids: list[uuid.UUID] | Type[Empty] = Empty,
        exclude_group_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> SpecializationGroupListResponse:
        path = "/api/rest/spec-groups/"
        params = {"query": query, "id": group_ids, "exclude_id": exclude_group_ids}
        params = {key: value for key, value in params.items() if value is not Empty}

        return await self.rest_get(
            path=path, response_model=SpecializationGroupListResponse, params=params
        )

    async def get_specializations(
            self,
            query: str | type[Empty] = Empty,
            group_id: uuid.UUID | Type[Empty] = Empty,
            specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            exclude_specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> SpecializationListResponse:
        path = "/api/rest/specializations/"
        params = {
            "query": query,
            "group_id": group_id,
            "id": specialization_ids,
            "exclude_id": exclude_specialization_ids,
        }
        params = {key: value for key, value in params.items() if value is not Empty}

        return await self.rest_get(
            path=path, response_model=SpecializationListResponse, params=params
        )

    async def get_skills(
            self,
            query: str | Type[Empty] = Empty,
            skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
            exclude_skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
    ) -> SkillListResponse:
        path = "/api/rest/skills/"
        params = {"query": query, "id": skill_ids, "exclude_id": exclude_skill_ids}
        params = {key: value for key, value in params.items() if value is not Empty}

        return await self.rest_get(path=path, response_model=SkillListResponse, params=params)
