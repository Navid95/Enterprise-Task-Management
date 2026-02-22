import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from sqlalchemy import insert

from src.app.user_management.domain.value_objects.user_info import (
    UserEmail,
    UserMobileNumber,
    HashedPassword,
    UserId,
)
from src.app.user_management.infrastructure.persistence.base import BaseModel
from src.app.user_management.infrastructure.persistence.models import UserModel


_DEFAULT_USER_EMAIL = UserEmail(email="default@persistance.com")
_DEFAULT_USER_MOBILE = UserMobileNumber(mobile="1234567890")
_DEFAULT_USER_HASHED_PASSWORD = HashedPassword(hashed_password="!@#$%^&*()_+")


@pytest_asyncio.fixture(scope="session")
async def engine():
    _engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
    )
    async with _engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield _engine
    await _engine.dispose()


@pytest_asyncio.fixture
async def session(engine) -> AsyncSession:
    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    async with async_session() as _session:
        yield _session
        await _session.rollback()


@pytest_asyncio.fixture
async def seeded_session(engine):
    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    async with async_session() as session:
        await session.execute(
            insert(UserModel.__table__).values(
                id=UserId().id,
                mobile_num=_DEFAULT_USER_MOBILE.mobile,
                email_address=_DEFAULT_USER_EMAIL.email,
                hashed_password=_DEFAULT_USER_HASHED_PASSWORD.hashed_password,
            )
        )
        await session.flush()
        yield session
        await session.rollback()
