import pytest

from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.value_objects.user_info import (
    UserEmail,
    UserMobileNumber,
    HashedPassword,
    UserId,
)
from src.app.container import Container

_DEFAULT_USER_EMAIL = UserEmail(email="default@company.com")
_DEFAULT_USER_MOBILE = UserMobileNumber(mobile="1234567890")
_DEFAULT_USER_HASHED_PASSWORD = HashedPassword(hashed_password="!@#$%^&*()_+")


@pytest.fixture()
def container():
    test_container = Container()
    yield test_container
    del test_container


@pytest.fixture()
def create_user_uc(container):
    yield container.create_user_uc


@pytest.fixture()
def create_user_seeded_uc(container):
    container.user_repo.save(
        User(
            id=UserId(),
            mobile_num=_DEFAULT_USER_MOBILE,
            email_address=_DEFAULT_USER_EMAIL,
            hashed_password=_DEFAULT_USER_HASHED_PASSWORD,
        )
    )
    yield container.create_user_uc


@pytest.fixture()
def user_application_service(container):
    yield container.user_application_service

