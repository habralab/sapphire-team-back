import fastapi

from sapphire.projects.api.rest.projects.dependencies import path_project_is_owner
from sapphire.projects.database.models import ParticipantStatusEnum, Project, ProjectStatusEnum
from sapphire.projects.database.service import ProjectsDatabaseService

from .schemas import CreateReviewRequest, ReviewResponse


async def create_review(
    request: fastapi.Request,
    project: Project = fastapi.Depends(path_project_is_owner),
    data: CreateReviewRequest = fastapi.Body(embed=False),
) -> ReviewResponse:
    database_service: ProjectsDatabaseService = request.app.service.database

    async with database_service.transaction() as session:
        participants = await database_service.get_participants(
            session=session,
            project=project,
            user_id=data.user_id,
        )
    if not participants:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Not found.",
        )
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
