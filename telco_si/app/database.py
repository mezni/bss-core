"""Asynchronous database engine, session factory, and connectivity check.

Satisfies FR-006: an async SQLModel/SQLAlchemy engine backed by asyncpg with
connection pooling and reusable session management for application code.
"""

from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel

from .config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency yielding a scoped async session."""
    async with async_session_factory() as session:
        yield session


async def check_connection() -> bool:
    """Return ``True`` when the database answers a live ``SELECT 1``."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


__all__ = [
    "SQLModel",
    "async_session_factory",
    "check_connection",
    "engine",
    "get_session",
]
