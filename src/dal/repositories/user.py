from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.exceptions import NotFoundError
from src.dal.models import User
from src.dal.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model: type[User] = User

    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def create(self, username: str) -> User:
        user = self.model(username=username)
        await self.upsert(user)
        return user

    async def get_by_username(self, username: str) -> UUID:
        statement = select(self.model).where(self.model.username == username)
        model = await self.get_by_statement(statement)
        if not model:
            raise NotFoundError(f"User with username {username} not found")
        return model.id
