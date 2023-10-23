import uuid

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
