from collections.abc import Sequence
from uuid import UUID

from pydantic import Field

from src.dal.models import Chat, Message
from src.schemas.mixins import BaseMixin, StrippingMixin
from src.schemas.services.user import UserId


class ChatId(StrippingMixin):
    id: UUID = Field(description="Chat identifier")


class ChatInput(StrippingMixin):
    name: str = Field(description="Chat name")
    is_private: bool = Field(default=False, description="Is chat private")


class ChatCreate(StrippingMixin):
    chat: ChatInput = Field(description="Chat data")
    owner: UserId = Field(description="Chat owner")
    members: list[UserId] = Field(default_factory=list, description="Chat members")


class ChatInviteCreate(StrippingMixin):
    chat: ChatId = Field(description="Chat")
    inviter: UserId = Field(description="Inviter")


class ChatConnect(StrippingMixin):
    chat: ChatId = Field(description="Chat")
    user: UserId = Field(description="User")


class ChatResponse(BaseMixin):
    last_messages: Sequence[Message] = Field(description="Last messages")
    unread_messages: Sequence[Message] = Field(description="Unread messages")
    unread_messages_count: int = Field(description="Unread messages count")


class ChatStatusResponse(BaseMixin):
    chat: Chat = Field(description="Chats")
    unread_messages_count: int = Field(description="Unread messages count")
