from datetime import UTC, datetime
from uuid import uuid4

from polyfactory.factories.pydantic_factory import ModelFactory

from src.core.settings import ServerSettings
from src.dal.models import Chat, Message, UserChat
from src.schemas.api import Body, Request, Response
from src.schemas.services import ChatConnect, ChatCreate, ChatResponse, ChatStatusResponse, MessageCreate


class BaseFactory:
    __random_seed__ = 1


class RequestFactory(BaseFactory, ModelFactory[Request]): ...


class ResponseFactory(BaseFactory, ModelFactory[Response]): ...


class BodyFactory(BaseFactory, ModelFactory[Body]): ...


class ServerSettingsFactory(BaseFactory, ModelFactory[ServerSettings]): ...


class MessageCreateFactory(BaseFactory, ModelFactory[MessageCreate]): ...


class ChatConnectFactory(BaseFactory, ModelFactory[ChatConnect]): ...


class MessageFactory(BaseFactory, ModelFactory[Message]): ...


class UserChatFactory(BaseFactory, ModelFactory[UserChat]): ...


class ChatCreateFactory(BaseFactory, ModelFactory[ChatCreate]): ...


class ChatResponseFactory(BaseFactory, ModelFactory[ChatResponse]): ...


class ChatFactory(ModelFactory[Chat]):
    __model__ = Chat

    id = uuid4
    name = "Test Chat"
    owner_id = uuid4
    is_private = False
    deleted = False
    created_at = datetime.now(UTC)


class ChatStatusResponseFactory(BaseFactory, ModelFactory[ChatStatusResponse]):
    __model__ = ChatStatusResponse

    chat = ChatFactory.build
    unread_messages_count = 3
