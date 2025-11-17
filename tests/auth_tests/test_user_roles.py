import pytest
from src.app.auth.users import User
from src.app.auth.exceptions import UserNotFoundAuthError
from src.app.auth.utilities import login_required


@login_required
def say_hi(*args, **kwargs):
    user: User | None = kwargs.get("user")
    print(f"\n*args -> {args}")
    print(f"**kwargs -> {kwargs}")
    print(f"Hi {user.mobile_num if user else 'User'} !")


def test_login_required_success():
    u1 = User(mobile_num="1234567890", hashed_password="1234567890", roles=[])
    say_hi(0, 1, 2, 3, user=u1, custom="custom")


def test_login_required_no_user_exception():
    with pytest.raises(Exception) as err:
        say_hi(0, 1, 2, 3, custom="custom")
    assert err.type == UserNotFoundAuthError


def test_login_required_none_user_exception():
    with pytest.raises(Exception) as err:
        say_hi(0, 1, 2, 3, custom="custom", user=None)
    assert err.type == UserNotFoundAuthError
