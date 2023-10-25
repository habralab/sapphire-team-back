import uuid
from datetime import datetime

from autotests.rest.client import BaseRestClient

from .models import CreateProjectRequest, HealthResponse, ProjectListResponse, ProjectResponse


class ProjectsRestClient(BaseRestClient):
    async def get_health(self) -> HealthResponse:
        path = "/api/v1beta/rest/health"

        return await self.rest_get(path=path, response_model=HealthResponse)

    async def get_projects(self) -> ProjectListResponse:
        path = "/api/v1beta/rest/projects/"

        return await self.rest_get(path=path, response_model=ProjectListResponse)

    async def create_project(
            self,
            name: str,
            owner_id: uuid.UUID,
            description: str | None = None,
            deadline: datetime | None = None,
    ) -> ProjectResponse:
        path = "/api/v1beta/rest/projects/"
        request = CreateProjectRequest(
            name=name,
            description=description,
            owner_id=owner_id,
            deadline=deadline,
        )

        return await self.rest_post(path=path, data=request, response_model=ProjectResponse)
