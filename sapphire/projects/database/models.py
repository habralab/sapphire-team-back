import enum
import uuid
from datetime import datetime

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class ProjectStatusEnum(str, enum.Enum):
    PREPARATION = "preparation"
    IN_WORK = "in_work"
    FINISHED = "finished"


class ParticipantStatusEnum(str, enum.Enum):
    REQUEST = "request"
    DECLINED = "declined"
    JOINED = "joined"
    LEFT = "left"


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    owner_id: Mapped[uuid.UUID]
    deadline: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    history: Mapped[list["ProjectHistory"]] = relationship(
        back_populates="project",
        order_by="desc(ProjectHistory.created_at)",
        lazy="joined",
    )
    positions: Mapped[list["Position"]] = relationship(back_populates="project", lazy="joined")


class ProjectHistory(Base):
    __tablename__ = "projects_history"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    status: Mapped[ProjectStatusEnum] = mapped_column(Enum(ProjectStatusEnum))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    project: Mapped[Project] = relationship(back_populates="history", lazy="joined")


class Position(Base):
    __tablename__ = "project_positions"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, unique=True)
    name = Mapped[str]
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), primary_key=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    closed_at: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    project: Mapped[Project] = relationship(back_populates="positions", lazy="joined")
    participants: Mapped[list["Participant"]] = relationship(back_populates="position",
                                                             lazy="joined")


class Participant(Base):
    __tablename__ = "project_participants"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    position_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("project_positions.id"),
                                                   primary_key=True)
    user_id: Mapped[uuid.UUID]
    status: Mapped[ParticipantStatusEnum] = mapped_column(Enum(ParticipantStatusEnum))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    position: Mapped[Position] = relationship(back_populates="participants", lazy="joined")
