from typing import Any

from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import NotFoundError
from src.core.logger import get_logger
from src.dal import ChatMessageRepository, ChatRepository, UserChatRepository, UserRepository
from src.helpers import get_current_timestamp
from src.schemas.api import Body, Response, StatusCode
from src.schemas.services import ChatConnect, ChatCreate, ChatResponse, ChatStatusResponse, UserId, UserInput

logger = get_logger("chat_service")


class ChatService:
    __slots__ = ("chat_message_repo", "chat_repo", "session", "user_chat_repo", "user_repo")

    def __init__(self, session: AsyncSession):
        self.session = session
        self.chat_repo = ChatRepository(session)
        self.user_chat_repo = UserChatRepository(session)
        self.chat_message_repo = ChatMessageRepository(session)
        self.user_repo = UserRepository(session)

    async def create_user(self, data: dict[str, Any]) -> Response:
        _data: UserInput = UserInput.model_validate(data)
        user = await self.user_repo.create(username=_data.username)
        return Response(
            status_code=StatusCode.CREATED, body=Body(details=f"user_id: {user.id}, username: {user.username}")
        )

    async def get_user_id(self, data: dict[str, Any]) -> Response:
        _data: UserInput = UserInput.model_validate(data)
        user_id = await self.user_repo.get_by_username(username=_data.username)
        return Response(status_code=StatusCode.OK, body=Body(details=user_id))

    async def create_chat(self, data: dict[str, Any]) -> Response:
        _data: ChatCreate = ChatCreate.model_validate(data)
        chat = await self.chat_repo.create(data=_data)

        _data.members.append(_data.owner)

        members = [user.id for user in _data.members]

        await self.user_chat_repo.add_members(user_ids=members, chat_id=chat.id)
        return Response(status_code=StatusCode.CREATED, body=Body(details=f"chat_id: {chat.id}, name: {chat.name}"))

    async def connect(self, data: dict[str, Any]) -> Response:
        _data: ChatConnect = ChatConnect.model_validate(data)
        chat = await self.chat_repo.get(_data.chat.id)
        if not chat:
            logger.warning("Chat with id %s not found", _data.chat.id)
            raise NotFoundError(f"Chat with id {_data.chat.id} not found")

        user_chat = await self.user_chat_repo.get_user_chat(_data.user.id, _data.chat.id)
        if not user_chat:
            logger.info("User %s not in chat %s, adding", _data.user.id, _data.chat.id)
            user_chat = await self.user_chat_repo.create(_data.user.id, _data.chat.id)
            await self.session.flush()
            await self.session.refresh(user_chat)

        last_n_messages = await self.chat_message_repo.get_last_messages(chat_id=chat.id)
        unread_messages = await self.chat_message_repo.get_unread_messages(
            chat_id=chat.id, last_seen=user_chat.last_seen
        )
        user_chat.last_seen = get_current_timestamp()
        await self.session.flush()
        await self.session.refresh(user_chat)

        return Response(
            status_code=StatusCode.OK,
            body=Body(
                details=ChatResponse(
                    last_messages=last_n_messages,
                    unread_messages_count=len(unread_messages),
                    unread_messages=unread_messages,
                )
            ),
        )

    async def get_status(self, data: dict[str, Any]) -> Response:
        __data: UserId = UserId.model_validate(data)
        user_chats = await self.user_chat_repo.get_user_chats(user_id=__data.id)
        if not user_chats:
            logger.warning("User with id %s has no chats", __data.id)
            raise NotFoundError(f"User with id {__data.id} has no chats")

        status = []
        for chat in user_chats:
            unread_messages_count = await self.user_chat_repo.get_unread_messages_count(
                user_id=__data.id, chat_id=chat.id
            )
            status.append(ChatStatusResponse(chat=chat, unread_messages_count=unread_messages_count))

        return Response(status_code=StatusCode.OK, body=Body(details=status))
