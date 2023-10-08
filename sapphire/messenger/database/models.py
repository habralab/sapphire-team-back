import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    is_personal: Mapped[bool]

    messages: Mapped[list["Message"]] = relationship(back_populates="chat")
    member: Mapped[list["Member"]] = relationship(back_populates="chat")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.id"))
    text: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)

    chat: Mapped[Chat] = relationship(Chat, back_populates="message")


class Member(Base):
    __tablename__ = "chat_members"

    user_id: Mapped[uuid.UUID]
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.id"), primary_key=True)
    leave_at: Mapped[datetime | None]
    join_at: Mapped[datetime] = mapped_column(default=datetime.now)

    chat: Mapped[Chat] = relationship(Chat, back_populates="member")
