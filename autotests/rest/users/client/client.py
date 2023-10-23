import io
import uuid
from typing import Set

from autotests.rest.client import BaseRestClient

from .models import HealthResponse, UserResponse, UserUpdateRequest


class UsersRestClient(BaseRestClient):
    
    async def get_health(self) -> HealthResponse:
        path = "/api/v1beta/rest/health"

        return await self.rest_get(path=path, response_model=HealthResponse)

    async def get_user(self, user_id: uuid.UUID) -> UserResponse:
        path = f"/api/v1beta/rest/users/{user_id}"

        return await self.rest_get(path=path, response_model=UserResponse)

    async def update_user(
            self,
            user_id: uuid.UUID,
            first_name: str | None = None,
            last_name: str | None = None,
            about: str | None = None,
            main_specialization_id: uuid.UUID | None = None,
            secondary_specialization_id: uuid.UUID | None = None,
    ) -> UserResponse:
        path = f"/api/v1beta/rest/users/{user_id}"
        request = UserUpdateRequest(
            first_name=first_name,
            last_name=last_name,
            about=about,
            main_specialization_id=main_specialization_id,
            secondary_specialization_id=secondary_specialization_id,
        )

        return await self.rest_post(path=path, response_model=UserResponse, data=request)

    async def get_user_avatar(self, user_id: uuid.UUID) -> io.BytesIO:
        path = f"/api/v1beta/rest/user/{user_id}/avatar"

        response = await self.get(url=path)

        return io.BytesIO(response.content)

    async def update_user_avatar(self, user_id: uuid.UUID, avatar: io.BytesIO) -> UserResponse:
        path = f"/api/v1beta/rest/users/{user_id}/avatar"
        
        return await self.rest_post(path=path, response_model=UserResponse, files={"file": avatar})

    async def remove_user_avatar(self, user_id: uuid.UUID) -> UserResponse:
        path = f"/api/v1beta/rest/users/{user_id}/avatar"

        return await self.rest_delete(path=path, response_model=UserResponse)

    async def get_user_skills(self, user_id: uuid.UUID) -> set[uuid.UUID]:
        path = f"/api/v1beta/rest/users/{user_id}/skills"

        response = await self.get(url=path)

        return {uuid.UUID(skill) for skill in response.json()}

    async def update_user_skills(
            self,
            user_id: uuid.UUID,
            skills: Set[uuid.UUID],
    ) -> set[uuid.UUID]:
        path = f"/api/v1beta/rest/users/{user_id}/skills"

        response = await self.post(url=path, json=skills)

        return {uuid.UUID(skill) for skill in response.json()}
