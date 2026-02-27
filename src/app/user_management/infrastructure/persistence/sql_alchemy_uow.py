from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.app.user_management.domain.ports.driven.unit_of_work import UnitOfWork
from src.app.user_management.domain.ports.driven.user_repo import UserRepository


class AsyncSQLUnitOfWork(UnitOfWork):

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        user_repo_factory: Callable[[AsyncSession], UserRepository],
    ):
        self._session_factory = session_factory
        self._user_repo_factory = user_repo_factory
        self._user_repo: UserRepository | None = None
        self._session: AsyncSession | None = None

    async def __aenter__(self):
        self._session = self._session_factory()
        self._user_repo = self._user_repo_factory(self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            if self._session is not None:
                await self._session.close()
                self._session = None
                self._user_repo = None

    @property
    def user_repo(self) -> UserRepository:
        if self._user_repo is None:
            raise RuntimeError("UOW not started")
        return self._user_repo

    async def commit(self):
        if self._session is None:
            raise RuntimeError("UOW not started")
        await self._session.commit()

    async def rollback(self):
        if self._session is None:
            raise RuntimeError("UOW not started")
        await self._session.rollback()

    async def flush(self):
        if self._session is None:
            raise RuntimeError("UOW not started")
        await self._session.flush()
