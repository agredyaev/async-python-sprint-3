from sqlmodel.ext.asyncio.session import AsyncSession

from src.dal.models import Chat, User
from src.dal.repositories.base import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    model: type[Chat] = Chat

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create(self, data) -> Chat:  # type: ignore[no-untyped-def]
        owner = await self.session.get(User, data.owner.id)
        if not owner:
            raise ValueError(f"User with id {data.owner.id} not found")

        chat = self.model(name=data.chat.name, owner_id=data.owner.id, is_private=data.chat.is_private)
        await self.upsert(chat)
        return chat
