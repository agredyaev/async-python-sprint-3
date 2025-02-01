from sqlmodel.ext.asyncio.session import AsyncSession

from src.dal.models import Chat, ChatInvite
from src.dal.repositories.base import BaseRepository


class ChatInviteRepository(BaseRepository[ChatInvite]):
    model: type[ChatInvite] = ChatInvite

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create(self, data) -> ChatInvite:  # type: ignore[no-untyped-def]
        chat = await self.session.get(Chat, data.chat_id)
        if not chat:
            raise ValueError(f"Chat with id {data.chat_id} not found")

        chat_invite = self.model(**data.model_dump())
        await self.upsert(chat_invite)
        return chat_invite

    async def get_by_token(self, token: str) -> ChatInvite | None:
        return await self.session.get(self.model, token)
