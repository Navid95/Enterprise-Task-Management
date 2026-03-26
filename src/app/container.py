from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.app.infrastructure.persistence.db.session import get_session_factory
from src.app.user_management.application.services.user_application_service import (
    UserApplicationService,
)
from src.app.user_management.domain.ports.driven.user_repo import UserRepository
from src.app.user_management.infrastructure.persistence.async_user_repo_sql import (
    AsyncSQLUserRepository,
)
from src.app.user_management.infrastructure.persistence.sql_alchemy_uow import (
    AsyncSQLUnitOfWork,
)
from src.app.user_management.application.ports.password_hasher import IPasswordHasher
from src.app.user_management.infrastructure.security.argon2_hasher import Argon2PasswordHasher


class Container:
    def __init__(self):
        # factories
        self._user_repo_factory: Callable[[AsyncSession], UserRepository] = AsyncSQLUserRepository
        self._session_factory: async_sessionmaker[AsyncSession] = get_session_factory()

        # Singletons
        self.password_hasher : IPasswordHasher = Argon2PasswordHasher()
        self.user_application_service: UserApplicationService = UserApplicationService(self.password_hasher)

    def get_user_application_service(self):
        return self.user_application_service

    def get_uow(self):
        return AsyncSQLUnitOfWork(
            session_factory=self._session_factory,
            user_repo_factory=self._user_repo_factory,
        )
