import uuid

import fastapi

from sapphire.common.jwt.dependencies.rest import auth_user_id
from sapphire.projects.api.rest.projects.dependencies import get_path_project
from sapphire.projects.api.rest.projects.positions.participants.dependencies import (
    get_path_participant,
)
from sapphire.projects.database.models import (
    Participant,
    ParticipantStatusEnum,
    Project,
    ProjectStatusEnum,
)
from sapphire.projects.database.service import ProjectsDatabaseService

from .schemas import CreateReviewRequest, ReviewResponse


async def create_review(
    request: fastapi.Request,
    project: Project = fastapi.Depends(get_path_project),
    participant: Participant = fastapi.Depends(get_path_participant),
    user_id: uuid.UUID = fastapi.Depends(auth_user_id),
    review_request: CreateReviewRequest = fastapi.Body(embed=False),
) -> ReviewResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    if project.owner_id == participant.user_id:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="The project owner cannot leave feedback to himself",
        )

    from_user_id = user_id
    if user_id == project.owner_id:
        to_user_id = participant.user_id
    elif user_id == participant.user_id:
        to_user_id = project.owner_id
    else:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="The user must be a participant of the project",
        )

    if (
        project.status == ProjectStatusEnum.FINISHED
        and participant.status == ParticipantStatusEnum.JOINED
    ) or participant.status == ParticipantStatusEnum.LEFT:
        async with database_service.transaction() as session:
            review = await database_service.get_review(
                session=session,
                project=project.id,
                participant=participant.id,
                from_user_id=from_user_id,
                to_user_id=to_user_id,
            )

            if review is not None:
                raise fastapi.HTTPException(
                    status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                    detail="There is already such a review",
                )

            review = await database_service.create_review(
                session=session,
                project=project,
                participant=participant,
                from_user_id=from_user_id,
                to_user_id=to_user_id,
                rate=review_request.rate,
                text=review_request.text,
            )
    else:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="The project is not yet finished or the participant has not yet left the team",
        )

    return ReviewResponse.model_validate(review)
