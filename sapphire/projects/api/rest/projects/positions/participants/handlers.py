import uuid
from collections import defaultdict

import fastapi

from sapphire.common.api.exceptions import HTTPForbidden
from sapphire.common.jwt.dependencies.rest import is_auth
from sapphire.common.jwt.models import JWTData
from sapphire.projects.api.rest.projects.dependencies import get_path_project
from sapphire.projects.api.rest.projects.positions.dependencies import get_path_position
from sapphire.projects.broker.service import ProjectsBrokerService
from sapphire.projects.database.models import Participant, ParticipantStatusEnum, Position, Project
from sapphire.projects.database.service import ProjectsDatabaseService

from .dependencies import get_path_participant
from .schemas import ProjectParticipantResponse, UpdateParticipantRequest


async def create_participant(
    request: fastapi.Request,
    position_id: uuid.UUID,
    jwt_data: JWTData = fastapi.Depends(is_auth),
    project: Project = fastapi.Depends(get_path_project),
    position: Position = fastapi.Depends(get_path_position),
) -> ProjectParticipantResponse:
    broker_service: ProjectsBrokerService = request.app.service.broker
    database_service: ProjectsDatabaseService = request.app.service.database

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
            position_id=position_id,
            user_id=jwt_data.user_id,
        )
        await broker_service.send_participant_requested(
            project=project,
            participant=participant,
        )
        await broker_service.send_create_chat(
            is_personal=True,
            members_ids=[project.owner_id, participant.user_id],
        )

    return ProjectParticipantResponse.model_validate(participant)


async def get_participant(
    participant: Participant = fastapi.Depends(get_path_participant),
) -> ProjectParticipantResponse:
    return ProjectParticipantResponse.model_validate(participant)


async def update_participant(
    request: fastapi.Request,
    data: UpdateParticipantRequest = fastapi.Body(...),
    jwt_data: JWTData = fastapi.Depends(is_auth),
    project: Project = fastapi.Depends(get_path_project),
    participant: Participant = fastapi.Depends(get_path_participant),
) -> ProjectParticipantResponse:
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

    participant_status_nodes[project.owner_id].update(project_owner_nodes)
    participant_status_nodes[participant.user_id].update(participant_nodes)

    required_statuses = participant_status_nodes.get(jwt_data.user_id, {}).get(data.status, ())

    if participant.status not in required_statuses:
        raise HTTPForbidden()

    async with database_service.transaction() as session:
        updated_participant_db = await database_service.update_participant_status(
            session=session,
            participant=participant,
            status=data.status,
        )

        notification_send_map = {
            ParticipantStatusEnum.JOINED: {
                participant.user_id: broker_service.send_participant_joined
            },
            ParticipantStatusEnum.DECLINED: {
                participant.user_id: broker_service.send_participant_declined,
                project.owner_id: broker_service.send_owner_declined
            },
            ParticipantStatusEnum.LEFT: {
                participant.user_id: broker_service.send_participant_left,
                project.owner_id: broker_service.send_owner_excluded
            }
        }
        participant_notification_send = (notification_send_map
            .get(data.status, {})
            .get(jwt_data.user_id, None)
        )
        if participant_notification_send:
            await participant_notification_send(
                project=project, participant=participant
            )

    return ProjectParticipantResponse.model_validate(updated_participant_db)
