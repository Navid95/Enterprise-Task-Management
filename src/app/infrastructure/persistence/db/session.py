from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.app.core.settings import settings

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def init_engine() -> None:
    """
    Call once on app startup.
    """
    global _engine, _session_factory
    if _engine is not None:
        return

    _engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        future=True,
    )
    _session_factory = async_sessionmaker(
        bind=_engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    if _session_factory is None:
        raise RuntimeError("DB not initialized. Call init_engine() on startup.")
    return _session_factory


async def close_engine() -> None:
    """
    Call once on app shutdown.
    """
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None


def get_engine():
    if _engine is None:
        raise RuntimeError("DB not initialized. Call init_engine() on startup.")
    return _engine
