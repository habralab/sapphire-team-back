import pathlib

from facet import ServiceMixin
from fast_grpc import FastGRPCService, StatusCode, grpc_method

from sapphire.common.internal_api.service import BaseInternalAPIService
from sapphire.storage.database.service import StorageDatabaseService
from sapphire.storage.settings import StorageSettings

from .models import (
    GetSkillRequest,
    GetSpecializationGroupRequest,
    GetSpecializationRequest,
    SkillResponse,
    SpecializationGroupResponse,
    SpecializationResponse,
)


class StorageGRPCService(FastGRPCService):
    name = "Storage"
    root_path = pathlib.Path(__file__).parent
    proto_path = root_path / "grpc"
    grpc_path = root_path / "grpc"

    def __init__(self, database: StorageDatabaseService):
        self._database = database

    @property
    def database(self):
        return self._database

    @grpc_method(name="GetSpecializationGroup")
    async def get_specialization_group(
            self,
            request: GetSpecializationGroupRequest,
            context,
    ) -> SpecializationGroupResponse:
        async with self._database.transaction() as session:
            specialization_group = await self._database.get_specialization_group(
                session=session,
                habr_id=request.habr_id,
            )

        if specialization_group is None:
            await context.abort(
                code=StatusCode.NOT_FOUND,
                details="Specialization group not found.",
            )

        return SpecializationGroupResponse(
            id=specialization_group.id,
            name=specialization_group.name,
            name_en=specialization_group.name_en,
            habr_id=specialization_group.habr_id,
        )

    @grpc_method(name="GetSpecialization")
    async def get_specialization(
            self,
            request: GetSpecializationRequest,
            context,
    ) -> SpecializationResponse:
        async with self._database.transaction() as session:
            specialization = await self._database.get_specialization(
                session=session,
                habr_id=request.habr_id,
            )

        if specialization is None:
            await context.abort(code=StatusCode.NOT_FOUND, details="Specialization not found.")

        return SpecializationResponse(
            id=specialization.id,
            name=specialization.name,
            name_en=specialization.name_en,
            habr_id=specialization.habr_id,
        )

    @grpc_method(name="GetSkill")
    async def get_skill(self, request: GetSkillRequest, context) -> SkillResponse:
        async with self._database.transaction() as session:
            skill = await self._database.get_skill(session=session, habr_id=request.habr_id)

        if skill is None:
            await context.abort(code=StatusCode.NOT_FOUND, details="Skill not found.")

        return SkillResponse(id=skill.id, name=skill.name, habr_id=skill.habr_id)


class StorageInternalAPIService(BaseInternalAPIService):
    def __init__(
            self,
            database: StorageDatabaseService,
            port: int = 50051,
            reflection: bool = False,
    ):
        self._database = database

        services = [
            StorageGRPCService(database),
        ]
        super().__init__(*services, port=port, reflection=reflection)

    @property
    def database(self) -> StorageDatabaseService:
        return self._database

    @property
    def dependencies(self) -> list[ServiceMixin]:
        return [
            self._database,
        ]


def get_service(
        database: StorageDatabaseService,
        settings: StorageSettings,
) -> StorageInternalAPIService:
    return StorageInternalAPIService(
        database=database,
        port=settings.grpc_port,
        reflection=settings.grpc_reflection,
    )
