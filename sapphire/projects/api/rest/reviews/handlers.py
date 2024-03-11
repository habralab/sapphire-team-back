import fastapi

from sapphire.common.api.exceptions import HTTPNotFound
from sapphire.database.models import ParticipantStatusEnum, ProjectStatusEnum
from sapphire.projects import database

from .schemas import CreateReviewRequest, ReviewResponse


async def create_review(
    request: fastapi.Request,
    data: CreateReviewRequest = fastapi.Body(embed=False),
) -> ReviewResponse:
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        project = await database_service.get_project(session=session, project_id=data.project_id)
        participants = await database_service.get_participants(
            session=session,
            project_id=data.project_id,
            user_id=data.user_id,
        )
    if not participants or project is None:
        raise HTTPNotFound()

    if (
        project.status != ProjectStatusEnum.FINISHED
        or not any(
            participant.status in [ParticipantStatusEnum.JOINED, ParticipantStatusEnum.LEFT]
            for participant in participants
        )
    ):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="The project is not yet finished or participant did not joined to the project.",
        )

    async with database_service.transaction() as session:
        review = await database_service.get_review(
            session=session,
            project=project,
            from_user_id=project.owner_id,
            to_user_id=data.user_id,
        )

        if review is not None:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_400_BAD_REQUEST,
                detail="There is already such a review",
            )

        review = await database_service.create_review(
            session=session,
            project=project,
            from_user_id=project.owner_id,
            to_user_id=data.user_id,
            rate=data.rate,
            text=data.text,
        )

    return ReviewResponse.model_validate(review)
