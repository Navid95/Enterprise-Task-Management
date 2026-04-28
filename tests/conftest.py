from pathlib import Path
from typing import Type

import pytest
import pytest_asyncio
from pytest import FixtureRequest, Item
from sqlalchemy import NullPool, delete, insert, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.core.settings import Settings
from src.app.infrastructure.persistence.base import BaseModel
from src.app.infrastructure.persistence.db.session import close_engine, get_engine, init_engine
from src.app.user_management.application.ports.auth_token_service import IAuthTokenService
from src.app.user_management.application.ports.password_hasher import IPasswordHasher
from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.ports.driven.unit_of_work import UnitOfWork
from src.app.user_management.domain.ports.driven.user_repo import UserRepository
from src.app.user_management.domain.value_objects.user_info import (
    UserEmail,
    UserId,
    UserMobileNumber,
)
from src.app.user_management.infrastructure.auth.jwt_token_service import JWTTokenService
from src.app.user_management.infrastructure.persistence.async_user_repo_sql import (
    AsyncSQLUserRepository,
)
from src.app.user_management.infrastructure.persistence.models import UserModel
from src.app.user_management.infrastructure.persistence.sql_alchemy_uow import (
    AsyncSQLUnitOfWork,
)
from src.app.user_management.infrastructure.security.argon2_hasher import Argon2PasswordHasher
from tests.user_management.adapters.driven.fake_user_repo import FakeUserRepoInMemory
from tests.user_management.infrastructure.auth.fake_token_service import FakeTokenService
from tests.user_management.infrastructure.persistence.fake_in_memory_uow import (
    FakeUnitOfWorkInMemory,
)
from tests.user_management.infrastructure.security.fake_password_hasher import FakePasswordHasher

TEST_DIR = Path(__file__).resolve().parents[0]
settings = Settings(_env_file=f"{TEST_DIR}/.env")

_DEFAULT_USER_EMAIL = UserEmail(email=settings.ADMIN_EMAIL)
_DEFAULT_USER_MOBILE = UserMobileNumber(mobile="1234567890")
# Only used in unit tests
_DEFAULT_USER_HASHED_PASSWORD = FakePasswordHasher().hash_password(settings.ADMIN_PASSWORD)
_DEFAULT_USER_PLAIN_PASSWORD = settings.ADMIN_PASSWORD


def pytest_runtest_setup(item: Item):
    is_unit = any(True for marker in item.iter_markers() if marker.name == "unit")
    is_integration = any(True for marker in item.iter_markers() if marker.name == "integration")
    if not (is_unit or is_integration):
        pytest.fail(
            f"Error on {item.nodeid}.The test should be marked with @pytest.mark.unit or"
            f" @pytest.mark.integration"
        )
    if is_integration and item.config.getoption("-m") not in ["integration"]:
        pytest.skip("Integration tests require -m integration")


@pytest.fixture(scope="session")
def mark(request: FixtureRequest):
    yield request.config.getoption("-m")


@pytest.fixture(scope="session")
def db_backend(mark):
    if mark == "integration":
        yield "postgres"
    else:
        yield "memory"


@pytest_asyncio.fixture(scope="session")
async def engine(db_backend):
    if db_backend in ["memory"]:
        yield None
    else:
        pool_class = None
        if db_backend == "postgres":
            db_url = settings.DATABASE_URL
            pool_class = NullPool
            sys_url = db_url.rsplit("/", 1)[0] + "/postgres"
            db_name = db_url.rsplit("/", 1)[1]
            _sys_engine = create_async_engine(
                sys_url, poolclass=NullPool, isolation_level="AUTOCOMMIT"
            )
            async with _sys_engine.connect() as conn:
                exists = await conn.execute(
                    text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": db_name}
                )
                if not exists.scalar():
                    await conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            await _sys_engine.dispose()
        init_engine(settings, pool_class)
        _engine = get_engine()
        async with _engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)
        yield _engine
        async with _engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
        await close_engine()


@pytest.fixture(scope="session")
def token_service(mark) -> IAuthTokenService:
    if mark == "integration":
        yield JWTTokenService(enc_key=settings.ENCRYPTION_KEY, expiry_minutes=10)
    else:
        yield FakeTokenService()


@pytest.fixture(scope="session")
def password_hasher(mark) -> IPasswordHasher:
    if mark == "integration":
        yield Argon2PasswordHasher()
    else:
        yield FakePasswordHasher()


@pytest.fixture(scope="session")
def session_factory(engine) -> async_sessionmaker:
    if engine is not None:
        async_session_maker = async_sessionmaker(
            get_engine(),
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
async def seeded_session(session, password_hasher: IPasswordHasher) -> AsyncSession:
    await session.execute(
        insert(UserModel.__table__).values(
            id=UserId().id,
            mobile_num=_DEFAULT_USER_MOBILE.mobile,
            email_address=_DEFAULT_USER_EMAIL.email,
            hashed_password=password_hasher.hash_password(
                _DEFAULT_USER_PLAIN_PASSWORD
            ).hashed_password,
        )
    )
    await session.flush()
    yield session


@pytest.fixture()
def user_repo_factory(db_backend) -> Type[UserRepository]:
    if db_backend in ["memory"]:
        yield FakeUserRepoInMemory
    else:
        yield AsyncSQLUserRepository


@pytest.fixture()
def user_repo(db_backend, session):
    if db_backend in ["memory"]:
        yield FakeUserRepoInMemory()
    else:
        yield AsyncSQLUserRepository(session)


@pytest_asyncio.fixture()
async def seeded_user_repo(user_repo, password_hasher: IPasswordHasher):
    await user_repo.save(
        User(
            id=UserId(),
            mobile_num=_DEFAULT_USER_MOBILE,
            email_address=_DEFAULT_USER_EMAIL,
            hashed_password=password_hasher.hash_password(
                _DEFAULT_USER_PLAIN_PASSWORD,
            ),
        )
    )
    yield user_repo


@pytest.fixture()
def uow(db_backend, user_repo_factory, session_factory) -> UnitOfWork:
    if db_backend in ["memory"]:
        yield FakeUnitOfWorkInMemory(user_repo_factory())
    else:
        yield AsyncSQLUnitOfWork(
            session_factory=session_factory, user_repo_factory=user_repo_factory
        )


@pytest_asyncio.fixture()
async def seeded_uow(uow: UnitOfWork, password_hasher: IPasswordHasher) -> UnitOfWork:
    async with uow:
        user = User(
            id=UserId(),
            mobile_num=_DEFAULT_USER_MOBILE,
            email_address=_DEFAULT_USER_EMAIL,
            hashed_password=password_hasher.hash_password(_DEFAULT_USER_PLAIN_PASSWORD),
        )
        await uow.user_repo.save(user)
        await uow.commit()
    yield uow

    if isinstance(uow, AsyncSQLUnitOfWork):
        async with uow:
            stm = delete(UserModel).where(UserModel.id == user.id.id)
            await uow._session.execute(stm)
            await uow.commit()
