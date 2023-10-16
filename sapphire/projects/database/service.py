import pathlib
import uuid
from datetime import datetime
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sapphire.common.database.service import BaseDatabaseService
from sapphire.common.database.utils import Empty
from sapphire.projects.settings import ProjectsSettings

from .models import (
    Participant,
    ParticipantStatusEnum,
    Project,
    ProjectHistory,
    ProjectStatusEnum,
    Position,
)


class ProjectsDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    async def create_project(
        self,
        session: AsyncSession,
        name: str,
        owner_id: uuid.UUID,
        description: str | None = None,
        deadline: datetime | None = None,
    ) -> Project:
        project = Project(
            name=name, owner_id=owner_id, description=description, deadline=deadline
        )
        history = ProjectHistory(project=project, status=ProjectStatusEnum.PREPARATION)

        session.add_all([project, history])

        return project

    async def get_project(
            self,
            session: AsyncSession,
            project_id: uuid.UUID | Type[Empty] = Empty,
    ) -> Project | None:
        filters = []
        if project_id is not Empty:
            filters.append(Project.id == project_id)

        statement = select(Project).where(*filters)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def create_project_position(
            self,
            session: AsyncSession,
            project: Project,
            name: str,
    ) -> Position:
        position = Position(project=project, name=name)

        session.add(position)

        return position

    async def get_participant(
        self,
        session: AsyncSession,
        participant_id: uuid.UUID | Type[Empty] = Empty,
        position_id: uuid.UUID | Type[Empty] = Empty,
        user_id: uuid.UUID | Type[Empty] = Empty,
    ) -> Participant | None:
        filters = []
        if participant_id is not None:
            filters.append(Participant.id == participant_id)
        if position_id is not None:
            filters.append(Participant.position_id == position_id)
        if user_id is not None:
            filters.append(Participant.user_id == user_id)
        stmt = select(Participant).where(*filters).order_by(Participant.created_at.desc())
        result = await session.execute(stmt)
        return result.scalars().first()

    async def create_participant(
        self,
        session: AsyncSession,
        position_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Participant:
        participant = Participant(
            user_id=user_id,
            position_id=position_id,
            status=ParticipantStatusEnum.REQUEST,
        )
        session.add(participant)

        return participant

    async def update_status(
        self,
        session: AsyncSession,
        participant: Participant,
        status: ParticipantStatusEnum,
    ) -> Participant:
        participant.status = status
        session.add(participant)

        return participant


def get_service(settings: ProjectsSettings) -> ProjectsDatabaseService:
    return ProjectsDatabaseService(dsn=str(settings.db_dsn))
