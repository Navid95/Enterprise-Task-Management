import pytest
import pytest_asyncio

from src.app.user_management.application.services.user_application_service import UserApplicationService
from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.value_objects.user_info import (
    UserEmail,
    UserMobileNumber,
    HashedPassword,
    UserId,
)
from tests.user_management.infrastructure.persistence.fake_in_memory_uow import FakeUnitOfWorkInMemory
from tests.user_management.adapters.driven.fake_user_repo import FakeUserRepoInMemory

_DEFAULT_USER_EMAIL = UserEmail(email="default@company.com")
_DEFAULT_USER_MOBILE = UserMobileNumber(mobile="1234567890")
_DEFAULT_USER_HASHED_PASSWORD = HashedPassword(hashed_password="!@#$%^&*()_+")


class TestContainer:
    def __init__(self):
        self._user_repo_factory = FakeUserRepoInMemory
        self.user_application_service: UserApplicationService = UserApplicationService()

    def get_user_application_service(self):
        return self.user_application_service

    def get_user_repo(self):
        return self._user_repo_factory()


@pytest.fixture()
def container():
    test_container = TestContainer()
    yield test_container
    del test_container


@pytest.fixture()
def create_user_uc(container):
    yield container.get_user_application_service().create_user_uc


@pytest.fixture()
def user_repo(container):
    yield container.get_user_repo()


@pytest_asyncio.fixture()
async def seeded_user_repo(container):
    repo = container.get_user_repo()
    await repo.save(
        User(
            id=UserId(),
            mobile_num=_DEFAULT_USER_MOBILE,
            email_address=_DEFAULT_USER_EMAIL,
            hashed_password=_DEFAULT_USER_HASHED_PASSWORD,
        )
    )
    yield repo


@pytest.fixture()
def user_application_service(container):
    yield container.get_user_application_service()


@pytest.fixture()
def uow(user_repo):
    yield FakeUnitOfWorkInMemory(user_repo)


@pytest.fixture()
def seeded_uow(seeded_user_repo):
    yield FakeUnitOfWorkInMemory(seeded_user_repo)
