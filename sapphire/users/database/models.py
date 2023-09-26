import datetime
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, DateTime, String, Text, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid4)
    email = Column(String, unique=True)
    first_name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    avatar = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    profile = relationship("Profile", back_populates="user")
    skills = relationship("UserSkill", back_populates="user")
    habr_sessions = relationship("HabrSession", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"

    user_id = Column(UUID, ForeignKey("users.id"), primary_key=True, default=uuid4)
    about = Column(Text, nullable=True)
    main_specialization_id = Column(UUID, default=uuid4)
    secondary_specialization_id = Column(UUID, default=uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="profile")


class UserSkill(Base):
    __tablename__ = "user_skills"

    user_id = Column(UUID, ForeignKey("users.id"), primary_key=True, default=uuid4)
    skill_id = Column(UUID, primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="skills")


class HabrSession(Base):
    __tablename__ = "habr_sessions"

    user_id = Column(UUID, ForeignKey("users.id"), primary_key=True)
    access_token = Column(String)
    expire_at = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="habr_sessions")
