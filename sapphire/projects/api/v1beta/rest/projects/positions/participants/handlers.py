import uuid

import fastapi

from sapphire.common.jwt.dependencies.rest import auth_user_id
from sapphire.projects.api.v1beta.rest.projects.positions.dependencies import check_path_position
from sapphire.projects.database.models import Participant, ParticipantStatusEnum, Position
from sapphire.projects.database.service import ProjectsDatabaseService

from .dependencies import check_path_participant
from .schemas import ProjectParticipantResponse


async def create_request_participate(
    request: fastapi.Request,
    position_id: uuid.UUID,
    user_id: uuid.UUID = fastapi.Depends(auth_user_id),
    position: Position = fastapi.Depends(check_path_position),
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


async def remove_request_participate(
    request: fastapi.Request,
    participant: Participant = fastapi.Depends(check_path_participant),
) -> ProjectParticipantResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    if participant.status == ParticipantStatusEnum.REQUEST:
        async with database_service.transaction() as session:
            declined_participant_db = await database_service.update_participant_status(
                session=session,
                participant=participant,
                status=ParticipantStatusEnum.DECLINED,
            )
    else:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Participant have not `request` status",
        )

    return ProjectParticipantResponse.model_validate(declined_participant_db)
