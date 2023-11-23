from collections import defaultdict

import fastapi

from sapphire.common.api.dependencies.pagination import Pagination, pagination
from sapphire.common.api.exceptions import HTTPForbidden, HTTPNotFound
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.projects.api.rest.projects.schemas import ParticipantResponse
from sapphire.projects.broker.service import ProjectsBrokerService
from sapphire.projects.database.models import Participant, ParticipantStatusEnum
from sapphire.projects.database.service import ProjectsDatabaseService

from .dependencies import get_path_participant
from .schemas import (
    CreateParticipantRequest,
    ParticipantListFiltersRequest,
    ParticipantListResponse,
    UpdateParticipantRequest,
)


async def create_participant(
    request: fastapi.Request,
    jwt_data: JWTData = fastapi.Depends(is_auth),
    data: CreateParticipantRequest = fastapi.Body(embed=False),
) -> ParticipantResponse:
    broker_service: ProjectsBrokerService = request.app.service.broker
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        position = await database_service.get_position(
            session=session,
            position_id=data.position_id,
        )

    if position is None:
        raise HTTPNotFound()

    async with database_service.transaction() as session:
        participant = await database_service.get_participant(
            session=session,
            position_id=position.id,
            user_id=jwt_data.user_id,
        )

    if participant and participant.status in (
        ParticipantStatusEnum.REQUEST,
        ParticipantStatusEnum.JOINED,
    ):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Participant already send request to project or joined in project",
        )

    async with database_service.transaction() as session:
        participant = await database_service.create_participant(
            session=session,
            position_id=position.id,
            user_id=jwt_data.user_id,
        )
        await broker_service.send_participant_requested(
            project=position.project,
            participant=participant,
        )
        await broker_service.send_create_chat(
            is_personal=True,
            members_ids=[position.project.owner_id, participant.user_id],
        )

    return ParticipantResponse.model_validate(participant)


async def get_participant(
    participant: Participant = fastapi.Depends(get_path_participant),
) -> ParticipantResponse:
    return ParticipantResponse.model_validate(participant)


async def update_participant(
    request: fastapi.Request,
    data: UpdateParticipantRequest = fastapi.Body(embed=False),
    jwt_data: JWTData = fastapi.Depends(is_auth),
    participant: Participant = fastapi.Depends(get_path_participant),
) -> ParticipantResponse:
    broker_service: ProjectsBrokerService = request.app.service.broker
    database_service: ProjectsDatabaseService = request.app.service.database

    project_owner_nodes = {
        # New expected status : Required current statuses
        ParticipantStatusEnum.DECLINED: [ParticipantStatusEnum.REQUEST],
        ParticipantStatusEnum.JOINED: [ParticipantStatusEnum.REQUEST],
        ParticipantStatusEnum.LEFT: [ParticipantStatusEnum.JOINED],
    }
    participant_nodes = {
        # New expected status : Required current statuses
        ParticipantStatusEnum.DECLINED: [ParticipantStatusEnum.REQUEST],
        ParticipantStatusEnum.LEFT: [ParticipantStatusEnum.JOINED],
    }

    participant_status_nodes = defaultdict(dict)

    participant_status_nodes[participant.position.project.owner_id].update(project_owner_nodes)
    participant_status_nodes[participant.user_id].update(participant_nodes)

    required_statuses = participant_status_nodes.get(jwt_data.user_id, {}).get(data.status, ())

    if participant.status not in required_statuses:
        raise HTTPForbidden()

    async with database_service.transaction() as session:
        participant = await database_service.update_participant_status(
            session=session,
            participant=participant,
            status=data.status,
        )
        project = await database_service.get_project(
            session=session,
            project_id=participant.position.project_id,
        )

        notification_send_map = {
            ParticipantStatusEnum.JOINED: {
                participant.user_id: broker_service.send_participant_joined,
            },
            ParticipantStatusEnum.DECLINED: {
                participant.user_id: broker_service.send_participant_declined,
                participant.position.project.owner_id: broker_service.send_owner_declined,
            },
            ParticipantStatusEnum.LEFT: {
                participant.user_id: broker_service.send_participant_left,
                participant.position.project.owner_id: broker_service.send_owner_excluded,
            }
        }
        participant_notification_send = (notification_send_map
            .get(data.status, {})
            .get(jwt_data.user_id, None)
        )
        if participant_notification_send:
            await participant_notification_send(project=project, participant=participant)

    return ParticipantResponse.model_validate(participant)


async def get_participants(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
    filters: ParticipantListFiltersRequest = fastapi.Depends(ParticipantListFiltersRequest),
):
    database_service: ProjectsDatabaseService = request.app.service.database
    async with database_service.transaction() as session:
        participants_db = await database_service.get_projects(
            session=session,
            page=pagination.page,
            per_page=pagination.per_page,
            **filters.model_dump(),
        )

    return ParticipantListResponse.model_validate(participants_db)
