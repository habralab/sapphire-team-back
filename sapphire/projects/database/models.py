import uuid
from datetime import datetime
from typing import Literal, get_args

from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

ProjectStatusEnum = Literal["activated", "deactivated"]
ParticipantStatusEnum = Literal["active", "inactive"]


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    name: Mapped[str | None]
    description: Mapped[str | None]
    owner_id: Mapped[uuid.UUID]
    deadline: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class History(Base):
    __tablename__ = "projects_history"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    status: Mapped[ProjectStatusEnum] = mapped_column(
        Enum(*get_args(ProjectStatusEnum),
             name="ProjectStatusEnum",
             create_constraint=True,
             validate_strings=True,
             )
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)


class Position(Base):
    __tablename__ = "project_positions"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, unique=True)
    name = Mapped[str | None]
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)


class Participant(Base):
    __tablename__ = "project_participants"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    position_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("project_positions.id"), primary_key=True)
    user_id: Mapped[uuid.UUID]
    status: Mapped[ParticipantStatusEnum] = mapped_column(
        Enum(*get_args(ParticipantStatusEnum),
             name="ParticipantStatusEnum",
             create_constraint=True,
             validate_strings=True,
             )
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
