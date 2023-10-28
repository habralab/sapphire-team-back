from autotests.clients.rest.base_client import BaseRestClient

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

    async def get_skills(self) -> SkillListResponse:
        path = "/api/rest/skills/"

        return await self.rest_get(path=path, response_model=SkillListResponse)
