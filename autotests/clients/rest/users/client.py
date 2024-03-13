import io
import uuid

import httpx

from autotests.clients.rest.base_client import BaseRestClient
from autotests.clients.rest.exceptions import ResponseException

from .models import (
    AuthorizeRequest,
    AuthorizeResponse,
    HealthResponse,
    JWTData,
    UserResponse,
    UserUpdateRequest,
)


class UsersRestClient(BaseRestClient):
    async def get_health(self) -> HealthResponse:
        path = "/health"

        return await self.rest_get(path=path, response_model=HealthResponse)

    async def oauth2_habr_authorize(self) -> httpx.Response:
        path = "/api/rest/auth/oauth2/habr/authorize"

        response = await self.get(url=path, follow_redirects=False)

        return response

    async def check_auth(self) -> JWTData:
        path = "/api/rest/auth/check"

        return await self.rest_get(path=path, response_model=JWTData)

    async def logout(self) -> httpx.Response:
        path = "/api/rest/auth/logout"

        response = await self.delete(url=path)
        if response.status_code // 100 != 2:
            raise ResponseException(status_code=response.status_code, body=response.content)

        return response

    async def sign_up(self, email: str, password: str) -> AuthorizeResponse:
        path = f"/api/rest/auth/signup"
        request = AuthorizeRequest(email=email, password=password)

        return await self.rest_post(path=path, response_model=AuthorizeResponse, data=request)
        
    async def sign_in(self, email: str, password: str) -> AuthorizeResponse:
        path = f"/api/rest/auth/signin"
        request = AuthorizeRequest(email=email, password=password)

        return await self.rest_post(path=path, response_model=AuthorizeResponse, data=request)

    async def get_user(self, user_id: uuid.UUID) -> UserResponse:
        path = f"/api/rest/users/{user_id}"

        return await self.rest_get(path=path, response_model=UserResponse)

    async def update_user(
            self,
            user_id: uuid.UUID,
            first_name: str,
            last_name: str,
            about: str | None = None,
            main_specialization_id: uuid.UUID | None = None,
            secondary_specialization_id: uuid.UUID | None = None,
    ) -> UserResponse:
        path = f"/api/rest/users/{user_id}"
        request = UserUpdateRequest(
            first_name=first_name,
            last_name=last_name,
            about=about,
            main_specialization_id=main_specialization_id,
            secondary_specialization_id=secondary_specialization_id,
        )

        return await self.rest_post(path=path, response_model=UserResponse, data=request)

    async def get_user_avatar(self, user_id: uuid.UUID) -> io.BytesIO:
        path = f"/api/rest/users/{user_id}/avatar"

        response = await self.get(url=path)
        if response.status_code // 100 != 2:
            raise ResponseException(status_code=response.status_code, body=response.content)

        return io.BytesIO(response.content)

    async def update_user_avatar(self, user_id: uuid.UUID, avatar: io.BytesIO) -> UserResponse:
        path = f"/api/rest/users/{user_id}/avatar"

        return await self.rest_post(
            path=path,
            response_model=UserResponse,
            files={"avatar": avatar},
        )

    async def remove_user_avatar(self, user_id: uuid.UUID) -> UserResponse:
        path = f"/api/rest/users/{user_id}/avatar"

        return await self.rest_delete(path=path, response_model=UserResponse)

    async def get_user_skills(self, user_id: uuid.UUID) -> set[uuid.UUID]:
        path = f"/api/rest/users/{user_id}/skills"

        response = await self.get(url=path)
        if response.status_code // 100 != 2:
            raise ResponseException(status_code=response.status_code, body=response.content)

        return {uuid.UUID(skill) for skill in response.json()}

    async def update_user_skills(
            self,
            user_id: uuid.UUID,
            skills: set[uuid.UUID],
    ) -> set[uuid.UUID]:
        path = f"/api/rest/users/{user_id}/skills"

        response = await self.post(url=path, json=list(map(str, skills)))
        if response.status_code // 100 != 2:
            raise ResponseException(status_code=response.status_code, body=response.content)

        return {uuid.UUID(skill) for skill in response.json()}
