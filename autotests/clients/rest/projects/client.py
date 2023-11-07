import uuid
from datetime import datetime
from typing import Type

from pydantic import conint

from autotests.clients.rest.base_client import BaseRestClient
from autotests.clients.rest.exceptions import ResponseException
from autotests.clients.rest.projects.enums import ParticipantStatusEnum, ProjectStatusEnum
from autotests.utils import Empty

from .models import (
    CreatePositionRequest,
    CreateProjectRequest,
    CreateReviewRequest,
    HealthResponse,
    ParticipantResponse,
    PositionListResponse,
    PositionResponse,
    ProjectListResponse,
    ProjectPartialUpdateRequest,
    ProjectResponse,
    ReviewResponse,
    UpdateParticipantRequest,
    UserStatisticResponse,
)


class ProjectsRestClient(BaseRestClient):
    async def get_health(self) -> HealthResponse:
        path = "/health"

        return await self.rest_get(path=path, response_model=HealthResponse)

    async def get_projects(
            self,
            text: str | Type[Empty] = Empty,
            owner_id: uuid.UUID | Type[Empty] = Empty,
            deadline: datetime | Type[Empty] = Empty,
            status: ProjectStatusEnum | Type[Empty] = Empty,
            position_is_closed: bool | Type[Empty] = Empty,
            position_skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
            position_specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            page: int = 1,
            per_page: int = 10,
    ) -> ProjectListResponse:
        path = "/api/rest/projects/"
        params = {
            "query_text": text,
            "owner_id": owner_id,
            "deadline": deadline,
            "status": status.value if status is not Empty else Empty,
            "position_is_closed": position_is_closed,
            "position_skill_ids": position_skill_ids,
            "position_specialization_ids": position_specialization_ids,
            "page": page,
            "per_page": per_page,
        }
        params = {key: value for key, value in params.items() if value is not Empty}
        return await self.rest_get(path=path, params=params, response_model=ProjectListResponse)

    async def create_project(
            self,
            name: str,
            owner_id: uuid.UUID | None = None,
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

    async def get_project(self, project_id: uuid.UUID) -> ProjectResponse:
        path = f"/api/rest/projects/{project_id}"

        return await self.rest_get(path=path, response_model=ProjectResponse)

    async def partial_update_project(
            self,
            project_id: uuid.UUID,
            name: str | Type[Empty] = Empty,
            owner_id: uuid.UUID | Type[Empty] = Empty,
            description: str | None | Type[Empty] = Empty,
            deadline: datetime | None | Type[Empty] = Empty,
            status: ProjectStatusEnum | Type[Empty] = Empty,
    ) -> ProjectResponse:
        path = f"/api/rest/projects/{project_id}"
        request = ProjectPartialUpdateRequest(status=status)

        return await self.rest_patch(path=path, data=request, response_model=ProjectResponse)

    async def get_project_positions(
            self,
            project_id: uuid.UUID,
    ) -> PositionListResponse:
        path = f"/api/rest/projects/{project_id}/positions/"

        return await self.rest_get(path=path, response_model=PositionListResponse)

    async def create_project_position(
            self,
            project_id: uuid.UUID,
            specialization_id: uuid.UUID,
    ) -> PositionResponse:
        path = f"/api/rest/projects/{project_id}/positions/"
        request = CreatePositionRequest(specialization_id=specialization_id)

        return await self.rest_post(path=path, data=request, response_model=PositionResponse)

    async def get_project_position(
            self,
            project_id: uuid.UUID,
            position_id: uuid.UUID,
    ) -> PositionResponse:
        path = f"/api/rest/projects/{project_id}/positions/{position_id}"

        return await self.rest_get(path=path, response_model=PositionResponse)

    async def remove_project_position(
            self,
            project_id: uuid.UUID,
            position_id: uuid.UUID,
    ) -> PositionResponse:
        path = f"/api/rest/projects/{project_id}/positions/{position_id}"

        return await self.rest_delete(path=path, response_model=PositionResponse)

    async def get_project_position_skills(self, project_id: uuid.UUID, position_id: uuid.UUID):
        path = f"/api/rest/projects/{project_id}/positions/{position_id}/skills/"

        response = await self.get(url=path)
        if response.status_code // 100 != 2:
            raise ResponseException(status_code=response.status_code, body=response.content)

        return {uuid.UUID(skill) for skill in response.json()}

    async def update_project_position_skills(
            self,
            project_id: uuid.UUID,
            position_id: uuid.UUID,
            skills: set[uuid.UUID] = frozenset(),
    ) -> set[uuid.UUID]:
        path = f"/api/rest/projects/{project_id}/positions/{position_id}/skills/"

        response = await self.post(url=path, json=list(map(str, skills)))
        if response.status_code // 100 != 2:
            raise ResponseException(status_code=response.status_code, body=response.content)

        return {uuid.UUID(skill) for skill in response.json()}

    async def create_request_to_join_project_position(
            self,
            project_id: uuid.UUID,
            position_id: uuid.UUID,
    ) -> ParticipantResponse:
        path = f"/api/rest/projects/{project_id}/positions/{position_id}/participants/"
        
        return await self.rest_post(path=path, response_model=ParticipantResponse)

    async def get_project_position_participant(
            self,
            project_id: uuid.UUID,
            position_id: uuid.UUID,
            participant_id: uuid.UUID,
    ) -> ParticipantResponse:
        path = (
            f"/api/rest/projects/{project_id}/positions/{position_id}/participants/{participant_id}"
        )

        return await self.rest_get(path=path, response_model=ParticipantResponse)

    async def update_project_position_participant(
            self,
            project_id: uuid.UUID,
            position_id: uuid.UUID,
            participant_id: uuid.UUID,
            status: ParticipantStatusEnum,
    ) -> ParticipantResponse:
        path = (
            f"/api/rest/projects/{project_id}/positions/{position_id}/participants/{participant_id}"
        )
        request = UpdateParticipantRequest(status=status)

        return await self.rest_post(path=path, data=request, response_model=ParticipantResponse)

    async def create_project_review(
            self,
            project_id: uuid.UUID,
            user_id: uuid.UUID,
            rate: conint(ge=1, le=5),
            text: str,
    ) -> ReviewResponse:
        path = f"/api/rest/projects/{project_id}/reviews/"
        request = CreateReviewRequest(
            user_id=user_id,
            rate=rate,
            text=text,
        )

        return await self.rest_post(path=path, data=request, response_model=ReviewResponse)

    async def get_user_statistic(self, user_id: uuid.UUID) -> UserStatisticResponse:
        path = f"/api/rest/users/{user_id}/statistic"

        return await self.rest_get(path=path, response_model=UserStatisticResponse)
