import uuid

import fastapi

from sapphire.common.api.jwt.depends import get_user_id
from sapphire.projects.database.service import ProjectsDatabaseService

from .schemas import ParticipantProjectResponse


async def validate_project_data_and_get_participant(
    database_service: ProjectsDatabaseService,
    project_id: uuid.UUID,
    position_id: uuid.UUID,
    user_id: uuid.UUID,
):
    async with database_service.transaction() as session:
        project_db = await database_service.get_project(
            session=session,
            id=project_id,
        )
        position_db = await database_service.get_position(
            session=session,
            project_id=project_id,
            position_id=position_id,
        )
        participant_db = await database_service.get_participant(
            session=session,
            position_id=position_id,
            user_id=user_id,
        )

    if project_db is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Project not found",
        )

    if position_db is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Position not found",
        )

    return participant_db


async def create_request_participate(
    request: fastapi.Request,
    project_id: uuid.UUID,
    position_id: uuid.UUID,
    user_id: uuid.UUID = fastapi.Depends(get_user_id),
) -> ParticipantProjectResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    participant_db = await validate_project_data_and_get_participant(
        database_service, project_id, position_id, user_id
    )

    if participant_db is not None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Participant already send request to project",
        )

    async with database_service.transaction() as session:
        created_participant_db = await database_service.create_request_participant(
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

    participant_db = await validate_project_data_and_get_participant(
        database_service, project_id, position_id, user_id
    )

    if participant_db is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Participant did not send request to project",
        )

    if not participant_db.status_is_request():
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Participant cannot remove request, because had different status",
        )

    async with database_service.transaction() as session:
        removed_participant_db = await database_service.remove_request_participant(
            session=session, participant=participant_db
        )

    return ParticipantProjectResponse.model_validate(removed_participant_db)
