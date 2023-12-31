import uuid

import backoff
from grpc.aio import AioRpcError

from sapphire.users.internal_api.models import GetUserRequest, UserResponse
from sapphire.users.internal_api.service import UsersGRPCService

from .settings import UsersInternalAPIClientSettings


class UsersInternalAPIClient(UsersGRPCService.Client):
    @backoff.on_exception(backoff.constant, AioRpcError, max_tries=3)
    async def get_user(self, user_id: uuid.UUID) -> UserResponse:
        request = GetUserRequest(id=user_id)
        return await super().get_user(request=request)


def get_client(settings: UsersInternalAPIClientSettings) -> UsersInternalAPIClient:
    return UsersInternalAPIClient(host=settings.users_grpc_host, port=settings.users_grpc_port)
