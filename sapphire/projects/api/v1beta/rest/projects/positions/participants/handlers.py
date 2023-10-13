import uuid

import fastapi

from sapphire.common.jwt.dependencies.websocket import get_user_id
from sapphire.projects.database.models import ParticipantStatusEnum
from sapphire.projects.database.service import ProjectsDatabaseService

from .schemas import ParticipantProjectResponse


async def create_request_participate(
    request: fastapi.Request,
    project_id: uuid.UUID,
    position_id: uuid.UUID,
    user_id: uuid.UUID = fastapi.Depends(get_user_id),
) -> ParticipantProjectResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        participant_db = await database_service.get_participant(
            session=session,
            position_id=position_id,
            user_id=user_id,
        )

    if participant_db is not None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Participant already send request to project",
        )

    async with database_service.transaction() as session:
        created_participant_db = await database_service.create_participant(
            session=session,
            position_id=position_id,
            user_id=user_id,
        )

    return ParticipantProjectResponse.model_validate(created_participant_db)


async def remove_request_participate(
    request: fastapi.Request,
    project_id: uuid.UUID,
    position_id: uuid.UUID,
    user_id: uuid.UUID = fastapi.Depends(get_user_id),
) -> ParticipantProjectResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        participant_db = await database_service.get_participant(
            session=session,
            position_id=position_id,
            user_id=user_id,
        )

    if participant_db is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Participant did not send request to project",
        )

    if participant_db.status != ParticipantStatusEnum.REQUEST:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Participant cannot remove request, because had different status",
        )

    async with database_service.transaction() as session:
        removed_participant_db = await database_service.remove_participant(
            session=session, participant=participant_db
        )

    return ParticipantProjectResponse.model_validate(removed_participant_db)
