class BaseUserManagementCTXError(Exception):
    """Base class for User Management context exceptions"""
    _DEFAULT_MESSAGE_: str = "User Management Error"
    _DEFAULT_STATUS_CODE_: int = 403

    def __init__(self, message: str = _DEFAULT_MESSAGE_, status_code: int = _DEFAULT_STATUS_CODE_):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class UnauthorizedAccessUserManagementCTXError(BaseUserManagementCTXError):
    _DEFAULT_MESSAGE_ = "Forbidden, insufficient permissions"
    _DEFAULT_STATUS_CODE_ = 403


class NotTeamManagerError(UnauthorizedAccessUserManagementCTXError):
    _DEFAULT_MESSAGE_ = "Operation can only be done by the Team's manager"


class MemberAlreadyInTeamError(BaseUserManagementCTXError):
    _DEFAULT_MESSAGE_ = "Member is already in the Team"
    _DEFAULT_STATUS_CODE_ = 409


class MemberNotInTeamError(BaseUserManagementCTXError):
    _DEFAULT_MESSAGE_ = "Member is not in the Team"
    _DEFAULT_STATUS_CODE_ = 409
