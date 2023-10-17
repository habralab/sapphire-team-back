import uuid

import fastapi

from sapphire.projects.database.models import Participant
from sapphire.projects.database.service import ProjectsDatabaseService


async def get_path_participant(
    request: fastapi.Request,
    participant_id: uuid.UUID = fastapi.Path(),
) -> Participant:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        db_position = await database_service.get_participant(
            session=session, participant_id=participant_id
        )
    if db_position is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Participant not found.",
        )

    return db_position


async def check_path_participant(
    participant: Participant = fastapi.Depends(get_path_participant),
    position_id: uuid.UUID = fastapi.Path()
) -> Participant:
    if participant.position_id != position_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Participant don't have retalionship with position."
        )

    return participant
