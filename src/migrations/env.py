import sys

from logging.config import fileConfig
from pathlib import Path

import asyncio
from typing import AnyStr

from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

import src.dal.models  # noqa: F401, E402

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = SQLModel.metadata


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode."""

    connectable = create_async_engine(config.get_section(config.config_ini_section).get("sqlalchemy.url"))

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection: AnyStr) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


run_migrations_online()
