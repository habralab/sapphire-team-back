import uuid
from datetime import datetime
from typing import Type

from autotests.clients.rest.base_client import BaseRestClient
from autotests.clients.rest.projects.enums import ParticipantStatusEnum, ProjectStatusEnum
from autotests.utils import Empty

from .models import (
    CreatePositionRequest,
    CreateProjectRequest,
    HealthResponse,
    ParticipantResponse,
    PositionResponse,
    ProjectListResponse,
    ProjectResponse,
    UpdateParticipantRequest,
)


class ProjectsRestClient(BaseRestClient):
    async def get_health(self) -> HealthResponse:
        path = "/health"

        return await self.rest_get(path=path, response_model=HealthResponse)

    async def get_projects(self) -> ProjectListResponse:
        path = "/api/rest/projects/"

        return await self.rest_get(path=path, response_model=ProjectListResponse)

    async def create_project(
            self,
            name: str,
            owner_id: uuid.UUID,
            description: str | None = None,
            deadline: datetime | None = None,
    ) -> ProjectResponse:
        path = "/api/rest/projects/"
        request = CreateProjectRequest(
            name=name,
            description=description,
            owner_id=owner_id,
            deadline=deadline,
        )

        return await self.rest_post(path=path, data=request, response_model=ProjectResponse)

    async def partial_update_project(
            self,
            project_id: uuid.UUID,
            name: str | Type[Empty] = Empty,
            owner_id: uuid.UUID | Type[Empty] = Empty,
            description: str | None | Type[Empty] = Empty,
            deadline: datetime | None | Type[Empty] = Empty,
            status: ProjectStatusEnum | Type[Empty] = Empty,
    ):
        raise NotImplementedError

    async def create_project_position(
            self,
            project_id: uuid.UUID,
            specialization_id: uuid.UUID,
    ) -> PositionResponse:
        path = f"/api/rest/projects/{project_id}/positions/"
        request = CreatePositionRequest(specialization_id=specialization_id)

        return await self.rest_post(path=path, data=request, response_model=PositionResponse)

    async def remove_project_position(
            self,
            project_id: uuid.UUID,
            position_id: uuid.UUID,
    ) -> PositionResponse:
        path = f"/api/rest/projects/{project_id}/positions/{position_id}"

        return await self.rest_delete(path=path, response_model=PositionResponse)

    async def create_request_to_join_project_position(
            self,
            project_id: uuid.UUID,
            position_id: uuid.UUID,
    ) -> ParticipantResponse:
        path = f"/api/rest/projects/{project_id}/positions/{position_id}/participants/"
        
        return await self.rest_post(path=path, response_model=ParticipantResponse)

    async def update_project_position_participant(
            self,
            project_id: uuid.UUID,
            position_id: uuid.UUID,
            participant_id: uuid.UUID,
            status: ParticipantStatusEnum,
    ) -> ParticipantResponse:
        path = (
            f"/api/rest/projects/{project_id}/positions/{position_id}/participants"
            f"/{participant_id}"
        )
        request = UpdateParticipantRequest(status=status)

        return await self.rest_post(path=path, data=request, response_model=ParticipantResponse)
