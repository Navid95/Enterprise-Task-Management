import pytest

from src.app.user_management.application.services.authentication_service import (
    AuthenticationService,
)
from src.app.user_management.application.services.user_application_service import (
    UserApplicationService,
)
from src.app.user_management.application.use_cases.create_user_use_case import (
    CreateUserUseCase,
)


@pytest.fixture()
def create_user_uc():
    yield CreateUserUseCase()


@pytest.fixture()
def user_application_service(password_hasher):
    yield UserApplicationService(password_hasher)


@pytest.fixture()
def authentication_service(token_service, password_hasher):
    yield AuthenticationService(token_service, password_hasher)
