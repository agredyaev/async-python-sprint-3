from typing import Any

from sqlmodel.ext.asyncio.session import AsyncSession

from src.dal import ChatMessageRepository, MessageRepository, UserChatRepository, UserMessageRepository
from src.schemas.api import Body, Response, StatusCode
from src.schemas.services import MessageCreate


class MessageService:
    __slots__ = ("chat_message_repo", "message_repo", "session", "user_chat_repo", "user_message_repo")

    def __init__(self, session: AsyncSession):
        self.session = session
        self.message_repo = MessageRepository(session)
        self.chat_message_repo = ChatMessageRepository(session)
        self.user_chat_repo = UserChatRepository(session)
        self.user_message_repo = UserMessageRepository(session)

    async def send_message(self, data: dict[str, Any]) -> Response:
        _data: MessageCreate = MessageCreate.model_validate(data)
        if not await self.user_chat_repo.get_user_chat(_data.connect.user.id, _data.connect.chat.id):
            return Response(status_code=StatusCode.BAD_REQUEST, body=Body(details="User is not a member of the chat"))

        message = await self.message_repo.create(content=_data.content)

        await self.chat_message_repo.create(chat_id=_data.connect.chat.id, message_id=message.id)
        await self.user_message_repo.create(user_id=_data.connect.user.id, message_id=message.id)

        return Response(status_code=StatusCode.OK, body=Body(details=f"message_id {message.id} is sent"))
