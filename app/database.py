from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


_connect_args: dict = {}
if settings.database_require_ssl:
    _connect_args["ssl"] = "require"

engine = create_async_engine(
    settings.database_url,
    echo=settings.is_development,
    connect_args=_connect_args,
    # Sized against Cloud SQL db-f1-micro's max_connections=25: at
    # Cloud Run maxScale=4, peak = 4 instances × (3+2) = 20 connections,
    # leaving ~5 for reserved roles / the migration job. Budget has to
    # change in lockstep with .github/workflows/deploy.yml --max-instances
    # and Cloud SQL's max_connections.
    pool_size=3,
    max_overflow=2,
    # pool_pre_ping replaces connections killed server-side (Cloud SQL
    # idle timeout, failover) before they surface as errors to the
    # caller. pool_recycle proactively retires connections before those
    # server-side timeouts fire.
    pool_pre_ping=True,
    pool_recycle=1800,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides an async database session."""
    async with async_session_maker() as session:
        yield session
