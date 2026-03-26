import pytest

from src.app.user_management.application.services.user_application_service import (
    UserApplicationService,
)
from src.app.user_management.application.use_cases.create_user_use_case import (
    CreateUserUseCase,
)

from tests.user_management.infrastructure.security.fake_password_hasher import FakePasswordHasher


@pytest.fixture()
def create_user_uc():
    yield CreateUserUseCase()


@pytest.fixture()
def user_application_service():
    yield UserApplicationService(FakePasswordHasher())
