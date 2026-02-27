from src.app.user_management.domain.ports.driven.unit_of_work import UnitOfWork
from src.app.user_management.domain.ports.driven.user_repo import UserRepository


class FakeUnitOfWorkInMemory(UnitOfWork):
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    @property
    def user_repo(self) -> UserRepository:
        return self._user_repo

    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()

    async def flush(self):
        pass
