from typing import Type

import pytest
import pytest_asyncio
from pytest import FixtureRequest
from sqlalchemy import NullPool, StaticPool, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.infrastructure.persistence.base import BaseModel
from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.ports.driven.unit_of_work import UnitOfWork
from src.app.user_management.domain.ports.driven.user_repo import UserRepository
from src.app.user_management.domain.value_objects.user_info import (
    HashedPassword,
    UserEmail,
    UserId,
    UserMobileNumber,
)
from src.app.user_management.infrastructure.persistence.async_user_repo_sql import (
    AsyncSQLUserRepository,
)
from src.app.user_management.infrastructure.persistence.models import UserModel
from src.app.user_management.infrastructure.persistence.sql_alchemy_uow import (
    AsyncSQLUnitOfWork,
)
from tests.user_management.adapters.driven.fake_user_repo import FakeUserRepoInMemory
from tests.user_management.infrastructure.persistence.fake_in_memory_uow import (
    FakeUnitOfWorkInMemory,
)

_DEFAULT_USER_EMAIL = UserEmail(email="default@persistance.com")
_DEFAULT_USER_MOBILE = UserMobileNumber(mobile="1234567890")
# Must be the upper-cased version of _DEFAULT_USER_PLAIN_PASSWORD (FakePasswordHasher upper cases)
_DEFAULT_USER_HASHED_PASSWORD = HashedPassword(hashed_password="!@#$%^&*()_+")
_DEFAULT_USER_PLAIN_PASSWORD = "!@#$%^&*()_+"


def pytest_addoption(parser):
    parser.addoption(
        "--db",
        action="store",
        default="memory",
        choices=("memory", "sqlite", "postgres"),
        help="Select  DB backend for tests.",
    )


@pytest.fixture(scope="session")
def db_backend(request: FixtureRequest):
    yield request.config.getoption("--db")


@pytest_asyncio.fixture(scope="session")
async def engine(db_backend):
    if db_backend == "memory":
        yield None
    else:
        db_url = ""
        pool_class = None
        if db_backend == "sqlite":
            db_url = "sqlite+aiosqlite:///:memory:"
            pool_class = StaticPool
        elif db_backend == "postgres":
            db_url = "postgresql+asyncpg://taskflow:taskflowpass@localhost:5433/taskflow_db"
            pool_class = NullPool
        _engine = create_async_engine(
            db_url,
            poolclass=pool_class,
        )
        async with _engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)
        yield _engine
        async with _engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
        await _engine.dispose()


@pytest.fixture(scope="session")
def session_factory(engine) -> async_sessionmaker:
    if engine is not None:
        async_session_maker = async_sessionmaker(
            engine,
            expire_on_commit=False,
        )
        yield async_session_maker
    else:
        yield


@pytest_asyncio.fixture()
async def session(session_factory) -> AsyncSession:
    if session_factory is not None:
        async with session_factory() as _session:
            yield _session
            await _session.rollback()
    else:
        yield


@pytest_asyncio.fixture()
async def seeded_session(session) -> AsyncSession:
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


@pytest.fixture()
def user_repo_factory(db_backend) -> Type[UserRepository]:
    if db_backend == "memory":
        yield FakeUserRepoInMemory
    else:
        yield AsyncSQLUserRepository


@pytest.fixture()
def user_repo(db_backend, session):
    if db_backend == "memory":
        yield FakeUserRepoInMemory()
    else:
        yield AsyncSQLUserRepository(session)


@pytest_asyncio.fixture()
async def seeded_user_repo(user_repo):
    await user_repo.save(
        User(
            id=UserId(),
            mobile_num=_DEFAULT_USER_MOBILE,
            email_address=_DEFAULT_USER_EMAIL,
            hashed_password=_DEFAULT_USER_HASHED_PASSWORD,
        )
    )
    yield user_repo


@pytest.fixture()
def uow(db_backend, user_repo_factory, session_factory) -> UnitOfWork:
    if db_backend == "memory":
        yield FakeUnitOfWorkInMemory(user_repo_factory())
    else:
        yield AsyncSQLUnitOfWork(
            session_factory=session_factory, user_repo_factory=user_repo_factory
        )


@pytest_asyncio.fixture()
async def seeded_uow(db_backend, uow) -> UnitOfWork:
    async with uow:
        user = User(
            id=UserId(),
            mobile_num=_DEFAULT_USER_MOBILE,
            email_address=_DEFAULT_USER_EMAIL,
            hashed_password=_DEFAULT_USER_HASHED_PASSWORD,
        )
        await uow.user_repo.save(user)
        await uow.commit()
    yield uow

    if db_backend != "memory":
        async with uow:
            stm = delete(UserModel).where(UserModel.id == user.id.id)
            await uow._session.execute(stm)
            await uow.commit()
