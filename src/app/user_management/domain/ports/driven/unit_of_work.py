from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from src.app.user_management.domain.ports.driven.user_repo import UserRepository


class UnitOfWork(AbstractAsyncContextManager):
    # Note: currently context specific, should evolve by project progress
    @property
    @abstractmethod
    def user_repo(self) -> UserRepository: ...

    @abstractmethod
    async def commit(self) -> None: ...
    @abstractmethod
    async def rollback(self) -> None: ...
    @abstractmethod
    async def flush(self) -> None: ...
    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...
