import pytest
from src.app.auth.users import User, Role
from src.app.auth.exceptions import UserNotFoundAuthError, UnauthorizedAccessAuthError
from src.app.auth.utilities import login_required, has_role


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


def test_has_role_success():
    u1: User = User(mobile_num="1234567890", hashed_password="1234567890", roles=[])
    r1: Role = Role(name="admin")
    u1.roles.append(r1)
    has_role(r1, u1)


def test_has_role_un_authorized_exception_wrong_role():
    u1: User = User(mobile_num="1234567890", hashed_password="1234567890", roles=[])
    r1: Role = Role(name="admin")
    r2: Role = Role(name="user")
    u1.roles.append(r1)
    with pytest.raises(Exception) as err:
        has_role(r2, u1)
    assert err.type == UnauthorizedAccessAuthError


def test_has_role_un_authorized_exception_no_role():
    u1: User = User(mobile_num="1234567890", hashed_password="1234567890", roles=[])
    r1: Role = Role(name="admin")
    with pytest.raises(Exception) as err:
        has_role(r1, u1)
    assert err.type == UnauthorizedAccessAuthError
