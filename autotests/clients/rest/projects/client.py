import io
import uuid
from datetime import datetime
from typing import Type

from pydantic import conint

from autotests.clients.rest.base_client import BaseRestClient
from autotests.clients.rest.exceptions import ResponseException
from autotests.clients.rest.projects.enums import ParticipantStatusEnum, ProjectStatusEnum
from autotests.utils import Empty

from .models import (
    CreateParticipantRequest,
    CreatePositionRequest,
    CreateProjectRequest,
    CreateReviewRequest,
    HealthResponse,
    ParticipantListResponse,
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
            query: str | Type[Empty] = Empty,
            owner_id: uuid.UUID | Type[Empty] = Empty,
            user_id: uuid.UUID | Type[Empty] = Empty,
            startline_ge: datetime | Type[Empty] = Empty,
            startline_le: datetime | Type[Empty] = Empty,
            deadline_ge: datetime | Type[Empty] = Empty,
            deadline_le: datetime | Type[Empty] = Empty,
            statuses: list[ProjectStatusEnum] | Type[Empty] = Empty,
            position_skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
            position_specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            participant_user_ids: list[uuid.UUID] | Type[Empty] = Empty,
            page: int = 1,
            per_page: int = 10,
    ) -> ProjectListResponse:
        path = "/api/rest/projects/"
        params = {
            "query": query,
            "owner_id": owner_id,
            "user_id": user_id,
            "startline_ge": startline_ge,
            "startline_le": startline_le,
            "deadline_ge": deadline_ge,
            "deadline_le": deadline_le,
            "status": [s.value for s in statuses] if statuses is not Empty else Empty,
            "position_skill_ids": position_skill_ids,
            "position_specialization_ids": position_specialization_ids,
            "participant_user_ids": participant_user_ids,
            "page": page,
            "per_page": per_page,
        }
        params = {key: value for key, value in params.items() if value is not Empty}
        return await self.rest_get(path=path, params=params, response_model=ProjectListResponse)

    async def create_project(
            self,
            name: str,
            owner_id: uuid.UUID,
            startline: datetime,
            description: str | None = None,
            deadline: datetime | None = None,
    ) -> ProjectResponse:
        path = "/api/rest/projects/"
        request = CreateProjectRequest(
            name=name,
            description=description,
            owner_id=owner_id,
            startline=startline,
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

    async def get_project_avatar(self, project_id: uuid.UUID) -> io.BytesIO:
        path = f"/api/rest/projects/{project_id}/avatar"

        response = await self.get(url=path)
        if response.status_code // 100 != 2:
            raise ResponseException(status_code=response.status_code, body=response.content)

        return io.BytesIO(response.content)

    async def upload_project_avatar(
            self,
            project_id: uuid.UUID,
            avatar: io.BytesIO,
    ) -> ProjectResponse:
        path = f"/api/rest/projects/{project_id}/avatar"

        return await self.rest_post(
            path=path,
            response_model=ProjectResponse,
            files={"avatar": avatar},
        )

    async def remove_project_avatar(self, project_id: uuid.UUID) -> ProjectResponse:
        path = f"/api/rest/projects/{project_id}/avatar"

        return await self.rest_delete(path=path, response_model=ProjectResponse)

    async def get_positions(
            self,
            project_id: uuid.UUID | Type[Empty] = Empty,
            specialization_ids: list[uuid.UUID] | Type[Empty] = Empty,
            skill_ids: list[uuid.UUID] | Type[Empty] = Empty,
            joined_user_id: uuid.UUID | Type[Empty] = Empty,
            query: str | Type[Empty] = Empty,
            project_startline_ge: datetime | Type[Empty] = Empty,
            project_startline_le: datetime | Type[Empty] = Empty,
            project_deadline_ge: datetime | Type[Empty] = Empty,
            project_deadline_le: datetime | Type[Empty] = Empty,
            project_statuses: list[ProjectStatusEnum] | Type[Empty] = Empty,
            page: int = 1,
            per_page: int = 10,
    ) -> PositionListResponse:
        path = f"/api/rest/positions/"
        params = {
            "project_id": project_id,
            "specialization_ids": specialization_ids,
            "skill_ids": skill_ids,
            "joined_user_id": joined_user_id,
            "query": query,
            "project_startline_ge": project_startline_ge,
            "project_startline_le": project_startline_le,
            "project_deadline_ge": project_deadline_ge,
            "project_deadline_le": project_deadline_le,
            "project_status": (
                Empty
                if project_statuses is Empty else
                [project_status.value for project_status in project_statuses]
            ),
            "page": page,
            "per_page": per_page,
        }
        params = {key: value for key, value in params.items() if value is not Empty}

        return await self.rest_get(path=path, params=params, response_model=PositionListResponse)

    async def create_position(
            self,
            project_id: uuid.UUID,
            specialization_id: uuid.UUID,
    ) -> PositionResponse:
        path = f"/api/rest/positions/"
        request = CreatePositionRequest(
            project_id=project_id,
            specialization_id=specialization_id,
        )

        return await self.rest_post(path=path, data=request, response_model=PositionResponse)

    async def get_position(self, position_id: uuid.UUID) -> PositionResponse:
        path = f"/api/rest/positions/{position_id}"

        return await self.rest_get(path=path, response_model=PositionResponse)

    async def remove_position(
            self,
            position_id: uuid.UUID,
    ) -> PositionResponse:
        path = f"/api/rest/positions/{position_id}"

        return await self.rest_delete(path=path, response_model=PositionResponse)

    async def get_position_skills(self, position_id: uuid.UUID):
        path = f"/api/rest/positions/{position_id}/skills/"

        response = await self.get(url=path)
        if response.status_code // 100 != 2:
            raise ResponseException(status_code=response.status_code, body=response.content)

        return {uuid.UUID(skill) for skill in response.json()}

    async def update_position_skills(
            self,
            position_id: uuid.UUID,
            skills: set[uuid.UUID] = frozenset(),
    ) -> set[uuid.UUID]:
        path = f"/api/rest/positions/{position_id}/skills/"

        response = await self.post(url=path, json=list(map(str, skills)))
        if response.status_code // 100 != 2:
            raise ResponseException(status_code=response.status_code, body=response.content)

        return {uuid.UUID(skill) for skill in response.json()}

    async def create_request_to_join_position(self, position_id: uuid.UUID) -> ParticipantResponse:
        path = f"/api/rest/participants/"
        request = CreateParticipantRequest(position_id=position_id)

        return await self.rest_post(path=path, data=request, response_model=ParticipantResponse)

    async def get_participant(self, participant_id: uuid.UUID) -> ParticipantResponse:
        path = f"/api/rest/participants/{participant_id}"

        return await self.rest_get(path=path, response_model=ParticipantResponse)

    async def update_participant(
            self,
            participant_id: uuid.UUID,
            status: ParticipantStatusEnum,
    ) -> ParticipantResponse:
        path = f"/api/rest/participants/{participant_id}"
        request = UpdateParticipantRequest(status=status)

        return await self.rest_post(path=path, data=request, response_model=ParticipantResponse)

    async def create_review(
            self,
            project_id: uuid.UUID,
            user_id: uuid.UUID,
            rate: conint(ge=1, le=5),
            text: str,
    ) -> ReviewResponse:
        path = f"/api/rest/reviews/"
        request = CreateReviewRequest(
            project_id=project_id,
            user_id=user_id,
            rate=rate,
            text=text,
        )

        return await self.rest_post(path=path, data=request, response_model=ReviewResponse)

    async def get_user_statistic(self, user_id: uuid.UUID) -> UserStatisticResponse:
        path = f"/api/rest/users/{user_id}/statistic"

        return await self.rest_get(path=path, response_model=UserStatisticResponse)

    async def get_participants(
            self,
            position_id: uuid.UUID | Type[Empty] = Empty,
            user_id: uuid.UUID | Type[Empty] = Empty,
            project_id: uuid.UUID | Type[Empty] = Empty,
            status: ParticipantStatusEnum | Type[Empty] = Empty,
            created_at_le: datetime | Type[Empty] = Empty,
            created_at_ge: datetime | Type[Empty] = Empty,
            joined_at_le: datetime | Type[Empty] = Empty,
            joined_at_ge: datetime | Type[Empty] = Empty,
            updated_at_le: datetime | Type[Empty] = Empty,
            updated_at_ge: datetime | Type[Empty] = Empty,
            page: int = 1,
            per_page: int = 10,
    ) -> ParticipantListResponse:
        path = "/api/rest/participants/"
        params = {
            "user_id": user_id,
            "position_id": position_id,
            "project_id": project_id,
            "status": status.value if status is not Empty else Empty,
            "created_at_le": created_at_le,
            "created_at_ge": created_at_ge,
            "joined_at_le": joined_at_le,
            "joined_at_ge": joined_at_ge,
            "updated_at_le": updated_at_le,
            "updated_at_ge":  updated_at_ge,
            "page": page,
            "per_page": per_page,
        }

        params = {key: value for key, value in params.items() if value is not Empty}
        return await self.rest_get(path=path, params=params, response_model=ParticipantListResponse)
