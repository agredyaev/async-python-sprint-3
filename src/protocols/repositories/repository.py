from typing import Protocol, TypeVar

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import Select

from src.dal.base import Base

T = TypeVar("T", bound=Base)


class RepositoryProtocol(Protocol[T]):
    async def upsert(self, obj: T) -> T: ...
    async def get(self, _id: UUID | tuple[UUID, UUID]) -> T | None: ...
    async def get_all(self, statement: Select) -> Sequence[T]: ...
    async def delete(self, _id: UUID) -> None: ...
