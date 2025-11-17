from functools import wraps
from src.app.auth.users import User
from src.app.auth.exceptions import UserNotFoundAuthError


def login_required(func):
    @wraps(func)
    def check_user(*args, user: User = None, **kwargs):
        if not user:
            raise UserNotFoundAuthError
        # TODO: Check user credentials/session
        return func(*args, user=user, **kwargs)

    return check_user
