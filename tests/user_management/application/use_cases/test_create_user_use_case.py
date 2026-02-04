import pytest
from src.app.user_management.domain.value_objects.user_info import (
    UserEmail,
    UserMobileNumber,
    HashedPassword,
)
from src.app.user_management.domain.exceptions import DuplicateUserInformation
from tests.user_management.application.conftest import (
    _DEFAULT_USER_EMAIL,
    _DEFAULT_USER_MOBILE,
    _DEFAULT_USER_HASHED_PASSWORD,
)


def test_create_user(create_user_uc):

    user = create_user_uc.execute(
        user_email=_DEFAULT_USER_EMAIL,
        user_mobile_number=_DEFAULT_USER_MOBILE,
        hashed_password=_DEFAULT_USER_HASHED_PASSWORD,
    )

    assert user.id is not None


def test_duplicate_user_mobile(create_user_seeded_uc):
    email = UserEmail(email="user1@company.com")
    mobile = _DEFAULT_USER_MOBILE
    hashed_passwd = HashedPassword(hashed_password="#!!$$#hsdvafb")

    with pytest.raises(DuplicateUserInformation) as e:
        user = create_user_seeded_uc.execute(
            user_email=email, user_mobile_number=mobile, hashed_password=hashed_passwd
        )
        assert e.context.get("user_mobile") == mobile


def test_duplicate_user_email(create_user_seeded_uc):
    email = _DEFAULT_USER_EMAIL
    mobile = UserMobileNumber(mobile="0000000000")
    hashed_passwd = HashedPassword(hashed_password="#!!$$#hsdvafb")

    with pytest.raises(DuplicateUserInformation) as e:
        user = create_user_seeded_uc.execute(
            user_email=email, user_mobile_number=mobile, hashed_password=hashed_passwd
        )
        assert e.context.get("user_email") == email
