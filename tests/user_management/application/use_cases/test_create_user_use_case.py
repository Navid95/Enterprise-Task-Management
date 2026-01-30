import pytest
from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.value_objects.user_info import (
    UserEmail,
    UserMobileNumber,
    UserId,
    HashedPassword,
)
from src.app.user_management.application.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from src.app.user_management.domain.exceptions import DuplicateUserInformation
from tests.user_management.adapters.driven.fake_user_repo import FakeUserRepoInMemory

_DEFAULT_USER_EMAIL = UserEmail(email="default@company.com")
_DEFAULT_USER_MOBILE = UserMobileNumber(mobile="1234567890")
_DEFAULT_USER_HASHED_PASSWORD = HashedPassword(hashed_password="!@#$%^&*()_+")


@pytest.fixture()
def create_user_use_case():
    repo = FakeUserRepoInMemory()
    repo.save(
        User(
            id=UserId(),
            mobile_num=_DEFAULT_USER_MOBILE,
            email_address=_DEFAULT_USER_EMAIL,
            hashed_password=_DEFAULT_USER_HASHED_PASSWORD,
        )
    )
    return CreateUserUseCase(repo)


def test_create_user(create_user_use_case):
    email = UserEmail(email="user1@company.com")
    mobile = UserMobileNumber(mobile="0000000000")
    hashed_passwd = HashedPassword(hashed_password="#!!$$#hsdvafb")

    user = create_user_use_case.execute(
        user_email=email, user_mobile_number=mobile, hashed_password=hashed_passwd
    )

    assert user.id is not None


def test_duplicate_user_mobile(create_user_use_case):
    email = UserEmail(email="user1@company.com")
    mobile = _DEFAULT_USER_MOBILE
    hashed_passwd = HashedPassword(hashed_password="#!!$$#hsdvafb")

    with pytest.raises(DuplicateUserInformation) as e:
        user = create_user_use_case.execute(
            user_email=email, user_mobile_number=mobile, hashed_password=hashed_passwd
        )
        assert e.context.get("user_mobile") == mobile


def test_duplicate_user_email(create_user_use_case):
    email = _DEFAULT_USER_EMAIL
    mobile = UserMobileNumber(mobile="0000000000")
    hashed_passwd = HashedPassword(hashed_password="#!!$$#hsdvafb")

    with pytest.raises(DuplicateUserInformation) as e:
        user = create_user_use_case.execute(
            user_email=email, user_mobile_number=mobile, hashed_password=hashed_passwd
        )
        assert e.context.get("user_email") == email
