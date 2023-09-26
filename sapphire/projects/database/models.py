from uuid import uuid4
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func


class ProjectStatusEnum(Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ParticipantStatusEnum(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(UUID, nullable=False)
    deadline = Column(DateTime(timezone=True))  # not sure in format
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class History(Base):
    __tablename__ = "projects_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    project_id = Column(UUID, ForeignKey("projects.id"))
    status = Column(ProjectStatusEnum('ProjectStatusEnum'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Position(Base):
    __tablename__ = "project_positions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    name = Column(String(255), nullable=False)
    project_id = Column(UUID, ForeignKey("projects.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class Participant(Base):
    __tablename__ = "project_participants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4())
    position_id = Column(UUID, ForeignKey("project_positions.id"))
    user_id = Column(UUID, nullable=False)
    status = Column(ParticipantStatusEnum('ParticipantStatusEnum'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
