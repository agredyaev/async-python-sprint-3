from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.logger import get_logger

logger = get_logger("db")


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    from src.core.settings import settings

    engine = create_async_engine(settings.db.url, echo=True)
    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    async with session_factory() as session, session.begin():
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            logger.exception(msg="Database error, rolling back transaction", exc_info=e)
            raise
