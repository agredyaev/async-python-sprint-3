from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field

from src.dal.base import Base
from src.helpers import get_current_timestamp


class IdMixin(Base):
    id: UUID = Field(default_factory=uuid4, primary_key=True, description="Unique identifier")


class CreatedAtMixin(Base):
    created_at: datetime = Field(default_factory=get_current_timestamp, description="Creation time")


class UserIdMixin(Base):
    user_id: UUID = Field(foreign_key="user.id", description="User identifier", ondelete="CASCADE")


class MessageIdMixin(Base):
    message_id: UUID = Field(foreign_key="message.id", description="Message identifier", ondelete="CASCADE")


class ChatIdMixin(Base):
    chat_id: UUID = Field(foreign_key="chat.id", description="Chat identifier", ondelete="CASCADE")


class SoftDeleteMixin(Base):
    deleted: bool = Field(default=False, description="Soft delete flag")


class OwnerIdMixin(Base):
    owner_id: UUID = Field(foreign_key="user.id", description="Owner identifier", ondelete="CASCADE")


class LastSeenMixin(Base):
    last_seen: datetime = Field(default_factory=get_current_timestamp, description="Last seen time")
