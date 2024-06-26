import uuid

import fastapi

from collabry.common.api.exceptions import HTTPNotFound
from collabry.database.models import Participant
from collabry.projects import database


async def get_path_participant(
    request: fastapi.Request,
    participant_id: uuid.UUID = fastapi.Path(),
) -> Participant:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        db_position = await database_service.get_participant(
            session=session,
            participant_id=participant_id,
        )
    if db_position is None:
        raise HTTPNotFound()

    return db_position
