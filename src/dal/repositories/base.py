from typing import Any, TypeVar

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import SelectBase
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.protocols import RepositoryProtocol

T = TypeVar("T", bound=Any)


class BaseRepository(RepositoryProtocol[T]):
    __slots__ = ("session",)

    model: type[T]

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def upsert(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def get(self, _id: UUID) -> T | None:
        return await self.session.get(self.model, _id)

    async def get_all(
        self, statement: SelectBase | None, order_by: SelectBase | None = None, limit: int | None = None
    ) -> Sequence[T]:
        if statement is None:
            statement = select(self.model)
        if order_by:
            statement = statement.order_by(order_by)
        if limit:
            statement = statement.limit(limit)

        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_by_statement(self, statement: SelectBase) -> T:
        result = await self.session.execute(statement)
        return result.scalar()

    async def delete(self, _id: UUID) -> None:
        obj = await self.session.get(self.model, _id)
        if obj:
            await self.session.delete(obj)
            await self.session.flush()

    async def bulk_create(self, objects: Sequence[T]) -> None:
        self.session.add_all(objects)
        await self.session.flush()

    async def exists(self, primary_keys: tuple[UUID, UUID]) -> bool:
        obj = await self.session.get(self.model, primary_keys)
        return bool(obj)
