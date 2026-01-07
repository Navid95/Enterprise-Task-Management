from functools import wraps
from src.app.domain.auth.users import User, Role
from src.app.domain.auth.exceptions import UserNotFoundAuthError, UnauthorizedAccessAuthError


def login_required(func):
    @wraps(func)
    def check_user(*args, user: User = None, **kwargs):
        if not user:
            raise UserNotFoundAuthError
        return func(*args, user=user, **kwargs)

    return check_user


def has_role(role: Role, user: User):
    if not (role and user) or (role not in user.roles):
        raise UnauthorizedAccessAuthError
