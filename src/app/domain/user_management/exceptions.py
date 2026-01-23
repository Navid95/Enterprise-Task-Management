class BaseAuthError(Exception):
    """Base class for authentication module exceptions"""
    _DEFAULT_MESSAGE_: str = "Authentication Error"
    _DEFAULT_STATUS_CODE_: int = 403

    def __init__(self, message: str = _DEFAULT_MESSAGE_, status_code: int = _DEFAULT_STATUS_CODE_):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class UserNotFoundAuthError(BaseAuthError):
    """When no authenticated user is found"""
    _DEFAULT_MESSAGE_ = "Authenticated user not found"
    _DEFAULT_STATUS_CODE_ = 401


class UnauthorizedAccessAuthError(BaseAuthError):
    _DEFAULT_MESSAGE_ = "Forbidden, insufficient permissions"
    _DEFAULT_STATUS_CODE_ = 403

