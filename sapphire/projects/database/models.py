from sqlalchemy import Column, String, Text, UUID, DateTime, ForeignKey, Null, Enum
from sqlalchemy.orm import declarative_base


class ProjectStatusEnum(Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ParticipantStatusEnum(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True)


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(UUID, nullable=False)
    deadline = Column(DateTime, default=Null)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class History(Base):
    __tablename__ = "projects_history"

    id = Column(UUID, primary_key=True)
    project_id = Column(UUID, ForeignKey("projects.id"))
    status = Column(ProjectStatusEnum('ProjectStatusEnum'), nullable=False)
    created_at = Column(DateTime, nullable=False)

class Position(Base):
    __tablename__ = "project_positions"

    id = Column(UUID, primary_key=True)
    project_id = Column(UUID, ForeignKey("projects.id"))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Participant(Base):
    __tablename__ = "project_participants"

    id = Column(UUID, primary_key=True)
    position_id = Column(UUID, ForeignKey("project_positions.id"))
    user_id = Column(UUID, ForeignKey("users.id"))
    status = Column(ParticipantStatusEnum('ParticipantStatusEnum'), nullable=False)
    created_at = Column(DateTime, nullable=False)   