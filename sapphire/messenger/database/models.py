import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_personal: Mapped[bool]

    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        order_by="desc(Message.created_at)",
    )
    last_message: Mapped["Message"] = relationship(
        back_populates="chat",
        order_by="desc(Message.created_at)",
        lazy=False,
        overlaps="messages",
    )
    members: Mapped[list["Member"]] = relationship(back_populates="chat", lazy=False)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.id"))
    user_id: Mapped[uuid.UUID]
    text: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    chat: Mapped[Chat] = relationship(Chat, back_populates="messages")


class Member(Base):
    __tablename__ = "chat_members"

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    user_id: Mapped[uuid.UUID]
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chats.id"))
    leave_at: Mapped[datetime | None]
    join_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    chat: Mapped[Chat] = relationship(Chat, back_populates="members")
