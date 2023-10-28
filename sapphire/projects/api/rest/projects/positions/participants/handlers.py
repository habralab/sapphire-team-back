import uuid
from collections import defaultdict

import fastapi

from sapphire.common.jwt.dependencies.rest import auth_user_id
from sapphire.projects.api.rest.projects.dependencies import get_path_project
from sapphire.projects.api.rest.projects.positions.dependencies import get_path_position
from sapphire.projects.database.models import Participant, ParticipantStatusEnum, Position, Project
from sapphire.projects.database.service import ProjectsDatabaseService

from .dependencies import get_path_participant
from .schemas import ProjectParticipantResponse, UpdateParticipantRequest


async def create_participant(
    request: fastapi.Request,
    position_id: uuid.UUID,
    user_id: uuid.UUID = fastapi.Depends(auth_user_id),
    position: Position = fastapi.Depends(get_path_position),
) -> ProjectParticipantResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        participant_db = await database_service.get_participant(
            session=session,
            position_id=position.id,
            user_id=user_id,
        )

    if participant_db and participant_db.status in (
        ParticipantStatusEnum.REQUEST,
        ParticipantStatusEnum.JOINED,
    ):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Participant already send request to project or joined in project",
        )

    async with database_service.transaction() as session:
        created_participant_db = await database_service.create_participant(
            session=session,
            position_id=position_id,
            user_id=user_id,
        )

    return ProjectParticipantResponse.model_validate(created_participant_db)


async def update_participant(
    request: fastapi.Request,
    data: UpdateParticipantRequest = fastapi.Body(...),
    request_user_id: uuid.UUID = fastapi.Depends(auth_user_id),
    project: Project = fastapi.Depends(get_path_project),
    participant: Participant = fastapi.Depends(get_path_participant),
) -> ProjectParticipantResponse:
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

    required_statuses = participant_status_nodes.get(request_user_id, {}).get(data.status, ())
    if participant.status in required_statuses:
        async with database_service.transaction() as session:
            updated_participant_db = await database_service.update_participant_status(
                session=session,
                participant=participant,
                status=data.status,
            )
    else:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Forbidden.",
        )

    return ProjectParticipantResponse.model_validate(updated_participant_db)
