import pathlib
import uuid
from datetime import datetime
from typing import Type

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sapphire.common.database.service import BaseDatabaseService
from sapphire.common.utils.empty import Empty
from sapphire.projects.settings import ProjectsSettings

from .models import (
    Base,
    Participant,
    ParticipantStatusEnum,
    Position,
    Project,
    ProjectHistory,
    ProjectStatusEnum,
)


class ProjectsDatabaseService(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    def get_fixtures_directory_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "fixtures"

    def get_models(self) -> list[Type[Base]]:
        return [Participant, Position, Project, ProjectHistory]

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
        return result.unique().scalar_one_or_none()

    async def update_project(
        self,
        session: AsyncSession,
        project: Project,
        name: str | None | Type[Empty] = Empty,
        owner_id: uuid.UUID | None | Type[Empty] = Empty,
        description: str | None | Type[Empty] = Empty,
        deadline: datetime | None | Type[Empty] = Empty,
        avatar: str | None | Type[Empty] = Empty,
    ) -> Project:
        query = select(Project).where(Project.id == project.id)
        result = await session.execute(query)
        project = result.scalar_one()

        if name is not Empty:
            project.name = name
        if owner_id is not Empty:
            project.owner_id = owner_id
        if description is not Empty:
            project.description = description
        if deadline is not Empty:
            project.deadline = deadline
        if avatar is not Empty:
            project.avatar = avatar

        return project

    async def get_project_positions(
            self,
            session: AsyncSession,
            project_id: uuid.UUID | Type[Empty] = Empty,
    ) -> list[Position]:
        filters = []
        if project_id is not Empty:
            filters.append(Position.project_id == project_id)

        statement = select(Position).where(*filters)
        result = await session.execute(statement)
        return list(result.scalars().all())

    async def get_project_position(
            self,
            session: AsyncSession,
            project_id: uuid.UUID | Type[Empty] = Empty,
            position_id: uuid.UUID | Type[Empty] = Empty,
    ) -> Position | None:
        filters = []
        if project_id is not Empty:
            filters.append(Position.project_id == project_id)
        if position_id is not Empty:
            filters.append(Position.id == position_id)

        statement = select(Position).where(*filters)
        result = await session.execute(statement)

        return result.unique().scalar_one_or_none()

    async def create_project_position(
            self,
            session: AsyncSession,
            project: Project,
    ) -> Position:
        position = Position(project=project)

        session.add(position)

        return position

    async def remove_project_position(self, session: AsyncSession, position: Position) -> Position:
        position.closed_at = datetime.now()

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
        if participant_id is not Empty:
            filters.append(Participant.id == participant_id)
        if position_id is not Empty:
            filters.append(Participant.position_id == position_id)
        if user_id is not Empty:
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

    async def update_participant_status(
        self,
        session: AsyncSession,
        participant: Participant,
        status: ParticipantStatusEnum,
    ) -> Participant:
        participant.status = status
        if status == ParticipantStatusEnum.JOINED:
            participant.joined_at = datetime.now()
        session.add(participant)

        return participant

    async def get_projects(
        self,
        session: AsyncSession,
        page: int | Type[Empty] = Empty,
        per_page: int | Type[Empty] = Empty,
    ) -> list[Project]:
        query = select(Project).order_by(desc(Project.created_at))

        if page is not Empty and per_page is not Empty:
            offset = (page - 1) * per_page
            query = query.limit(per_page).offset(offset)
        result = await session.execute(query)

        return list(result.unique().scalars().all())


def get_service(settings: ProjectsSettings) -> ProjectsDatabaseService:
    return ProjectsDatabaseService(dsn=str(settings.db_dsn))
