import os
import sys

from pathlib import Path

import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.settings import settings
from src.dal.base import Base

current_dir = Path(__file__).resolve().parent.parent
os.environ["PYTHONPATH"] = current_dir.as_uri()

sys.path.append(str(current_dir))


@pytest.fixture
def default_settings():
    return settings


@pytest_asyncio.fixture(autouse=True)
async def setup_test_database():
    """Create test database and tables."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False})

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_session():
    """Create async database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False})
    async with AsyncSession(engine) as session:
        yield session
