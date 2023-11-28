import pathlib

from facet import ServiceMixin
from fast_grpc import FastGRPCService, StatusCode, grpc_method

from sapphire.common.internal_api.service import BaseInternalAPIService
from sapphire.users.database.service import UsersDatabaseService
from sapphire.users.settings import UsersSettings

from .models import GetUserRequest, UserResponse


class UsersGRPCService(FastGRPCService):
    name = "Users"
    root_path = pathlib.Path(__file__).parent
    proto_path = root_path / "grpc"
    grpc_path = root_path / "grpc"

    def __init__(self, database: UsersDatabaseService):
        self._database = database

    @property
    def database(self):
        return self._database

    @grpc_method(name="GetUser")
    async def get_user(self, request: GetUserRequest, context) -> UserResponse:
        async with self.database.transaction() as session:
            user = await self.database.get_user(session=session, user_id=request.id)

        if user is None:
            await context.abort(code=StatusCode.NOT_FOUND, details="User not found.")

        return UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_activated=user.is_activated,
            about=user.profile.about,
            main_specialization_id=user.profile.main_specialization_id,
            secondary_specialization_id=user.profile.secondary_specialization_id,
        )


class UsersInternalAPIService(BaseInternalAPIService):
    def __init__(self, database: UsersDatabaseService, port: int = 50051, reflection: bool = False):
        self._database = database

        services = [
            UsersGRPCService(database),
        ]
        super().__init__(*services, port=port, reflection=reflection)

    @property
    def database(self):
        return self._database

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._database,
        ]


def get_service(
        database: UsersDatabaseService,
        settings: UsersSettings,
) -> UsersInternalAPIService:
    return UsersInternalAPIService(
        database=database,
        port=settings.grpc_port,
        # reflection=settings.grpc_reflection,
        reflection=True,
    )
